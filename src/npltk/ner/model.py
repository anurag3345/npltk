from __future__ import annotations

from typing import Any, cast

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchcrf import CRF


class CharCNNEncoder(nn.Module):
    def __init__(
        self,
        char_vocab_size: int,
        char_emb_dim: int = 64,
        out_channels: int = 64,
        kernel_size: int = 3,
        padding_idx: int = 0,
    ) -> None:
        super().__init__()
        self.char_emb = nn.Embedding(
            num_embeddings=char_vocab_size,
            embedding_dim=char_emb_dim,
            padding_idx=padding_idx,
        )
        self.conv = nn.Conv1d(
            in_channels=char_emb_dim,
            out_channels=out_channels,
            kernel_size=kernel_size,
            padding=kernel_size // 2,
        )

    def forward(self, char_ids: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, word_len = char_ids.size()

        x = char_ids.reshape(batch_size * seq_len, word_len)
        x = self.char_emb(x)
        x = x.transpose(1, 2)
        x = self.conv(x)
        x = F.relu(x)
        x, _ = torch.max(x, dim=2)
        x = x.reshape(batch_size, seq_len, -1)

        return x


class BiLSTMCRFNER(nn.Module):
    def __init__(
        self,
        word_vocab_size: int,
        char_vocab_size: int,
        num_labels: int,
        token_emb_dim: int = 256,
        char_emb_dim: int = 64,
        char_cnn_out: int = 64,
        char_kernel_size: int = 3,
        word_hidden_dim: int = 256,
        word_lstm_layers: int = 2,
        dropout: float = 0.3,
        padding_idx: int = 0,
    ) -> None:
        super().__init__()

        self.word_emb = nn.Embedding(
            num_embeddings=word_vocab_size,
            embedding_dim=token_emb_dim,
            padding_idx=padding_idx,
        )

        self.char_encoder = CharCNNEncoder(
            char_vocab_size=char_vocab_size,
            char_emb_dim=char_emb_dim,
            out_channels=char_cnn_out,
            kernel_size=char_kernel_size,
            padding_idx=padding_idx,
        )

        lstm_input_dim = token_emb_dim + char_cnn_out

        self.bilstm = nn.LSTM(
            input_size=lstm_input_dim,
            hidden_size=word_hidden_dim,
            num_layers=word_lstm_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if word_lstm_layers > 1 else 0.0,
        )

        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(word_hidden_dim * 2, num_labels)
        self.crf = CRF(num_labels)

    def forward(
        self,
        token_ids: torch.Tensor,
        char_ids: torch.Tensor,
        mask: torch.Tensor,
        labels: torch.Tensor | None = None,
    ) -> torch.Tensor | list[list[int]]:
        word_features = self.word_emb(token_ids)
        char_features = self.char_encoder(char_ids)

        x = torch.cat([word_features, char_features], dim=-1)
        x, _ = self.bilstm(x)
        x = self.dropout(x)

        emissions = self.classifier(x)
        mask = mask.bool()

        crf = cast(Any, self.crf)

        if labels is not None:
            loss = -crf(emissions, labels, mask).mean()
            return loss

        predictions = crf.viterbi_decode(emissions, mask)
        return predictions