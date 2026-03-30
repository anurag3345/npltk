from __future__ import annotations

import os
from typing import Any, Literal, cast

import torch
from npltk.tokenizer.factory import create_tokenizer

from .model import BiLSTMCRFNER

TokenizerMode = Literal["hybrid", "rule"]


class NERTagger:
    def __init__(
        self,
        model_path: str | None = None,
        device: str | None = None,
        tokenizer: Any | None = None,
        tokenizer_mode: TokenizerMode = "hybrid",
    ) -> None:
        base_dir = os.path.dirname(__file__)
        self.model_path = model_path or os.path.join(
            base_dir, "models", "ner_model.pth"
        )

        self.device = torch.device(
            device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        self.tokenizer = tokenizer or create_tokenizer(mode=tokenizer_mode)

        self.model: BiLSTMCRFNER | None = None
        self.word2id: dict[str, int] = {}
        self.char2id: dict[str, int] = {}
        self.label2id: dict[str, int] = {}
        self.id2label: dict[int, str] = {}
        self.config: dict[str, Any] = {}

        self._load()

    def _load(self) -> None:
        checkpoint = torch.load(self.model_path, map_location=self.device)

        self.word2id = checkpoint["word2id"]
        self.char2id = checkpoint["char2id"]
        self.label2id = checkpoint["label2id"]
        self.id2label = checkpoint["id2label"]
        self.config = checkpoint["config"]

        self.model = BiLSTMCRFNER(
            word_vocab_size=len(self.word2id),
            char_vocab_size=len(self.char2id),
            num_labels=len(self.label2id),
            token_emb_dim=self.config["token_emb_dim"],
            char_emb_dim=self.config["char_emb_dim"],
            char_cnn_out=self.config["char_cnn_out"],
            char_kernel_size=self.config["char_kernel_size"],
            word_hidden_dim=self.config["word_hidden_dim"],
            word_lstm_layers=self.config["word_lstm_layers"],
            dropout=self.config["dropout"],
            padding_idx=self.word2id["<PAD>"],
        ).to(self.device)

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    def _tokenize(self, text: str) -> list[str]:
        token_objs = self.tokenizer.tokenize(text)
        return [tok.text for tok in token_objs]

    def _encode_tokens(self, tokens: list[str]) -> list[int]:
        unk_id = self.word2id["<UNK>"]
        return [self.word2id.get(token, unk_id) for token in tokens]

    def _encode_chars(self, tokens: list[str]) -> list[list[int]]:
        max_word_len = self.config["max_word_len"]
        pad_id = self.char2id["<PAD>"]
        unk_id = self.char2id["<UNK>"]

        encoded: list[list[int]] = []
        for token in tokens:
            char_ids = [self.char2id.get(ch, unk_id) for ch in token[:max_word_len]]
            if len(char_ids) < max_word_len:
                char_ids += [pad_id] * (max_word_len - len(char_ids))
            encoded.append(char_ids)

        return encoded

    def _bio_to_entities(
        self, tokens: list[str], tags: list[str]
    ) -> list[dict[str, Any]]:
        entities: list[dict[str, Any]] = []
        current_tokens: list[str] = []
        current_type: str | None = None
        start_idx: int | None = None

        for i, (token, tag) in enumerate(zip(tokens, tags)):
            if tag == "O":
                if current_tokens:
                    entities.append(
                        {
                            "text": " ".join(current_tokens),
                            "label": current_type,
                            "start": start_idx,
                            "end": i - 1,
                        }
                    )
                    current_tokens = []
                    current_type = None
                    start_idx = None
                continue

            if "-" not in tag:
                if current_tokens:
                    entities.append(
                        {
                            "text": " ".join(current_tokens),
                            "label": current_type,
                            "start": start_idx,
                            "end": i - 1,
                        }
                    )
                    current_tokens = []
                    current_type = None
                    start_idx = None
                continue

            prefix, ent_type = tag.split("-", 1)

            if prefix == "B":
                if current_tokens:
                    entities.append(
                        {
                            "text": " ".join(current_tokens),
                            "label": current_type,
                            "start": start_idx,
                            "end": i - 1,
                        }
                    )
                current_tokens = [token]
                current_type = ent_type
                start_idx = i

            elif prefix == "I":
                if current_tokens and current_type == ent_type:
                    current_tokens.append(token)
                else:
                    current_tokens = [token]
                    current_type = ent_type
                    start_idx = i
            else:
                if current_tokens:
                    entities.append(
                        {
                            "text": " ".join(current_tokens),
                            "label": current_type,
                            "start": start_idx,
                            "end": i - 1,
                        }
                    )
                    current_tokens = []
                    current_type = None
                    start_idx = None

        if current_tokens:
            entities.append(
                {
                    "text": " ".join(current_tokens),
                    "label": current_type,
                    "start": start_idx,
                    "end": len(tokens) - 1,
                }
            )

        return entities

    def predict(self, text: str) -> dict[str, Any]:
        tokens = self._tokenize(text)
        if not tokens:
            return {"tokens": [], "tags": [], "entities": []}

        token_ids = self._encode_tokens(tokens)
        char_ids = self._encode_chars(tokens)

        token_tensor = torch.tensor([token_ids], dtype=torch.long).to(self.device)
        char_tensor = torch.tensor([char_ids], dtype=torch.long).to(self.device)
        mask = (token_tensor != self.word2id["<PAD>"]).bool().to(self.device)

        model = cast(BiLSTMCRFNER, self.model)

        with torch.no_grad():
            pred_ids = model(token_tensor, char_tensor, mask)[0]

        tags = [self.id2label[i] for i in pred_ids]
        entities = self._bio_to_entities(tokens, tags)

        return {
            "tokens": tokens,
            "tags": tags,
            "entities": entities,
        }

    def tag(self, text: str) -> list[tuple[str, str]]:
        result = self.predict(text)
        return list(zip(result["tokens"], result["tags"]))

    def extract(self, text: str) -> list[dict[str, Any]]:
        return self.predict(text)["entities"]