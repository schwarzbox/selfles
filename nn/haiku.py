#!/usr/bin/env python3
# IBOT

import logging

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

logging.basicConfig(level=logging.INFO)

# [BATCH_SIZE x SEQ_LEN x 1]
SEQ_LEN = 256
BATCH_SIZE = 1

char_to_idx = {
    ' ': 0, 'о': 1, 'е': 2, '\n': 3, 'а': 4, 'и': 5, 'н': 6, 'т': 7, 'л': 8, 'с': 9, 'р': 10, 'в': 11, '.': 12, 'к': 13, 'у': 14, 'д': 15, 'м': 16, 'п': 17, 'ы': 18, 'я': 19, 'ь': 20, 'й': 21, 'г': 22, 'з': 23, 'б': 24, 'ч': 25, ',': 26, 'х': 27, 'ш': 28, 'ж': 29, 'В': 30, '-': 31, 'ю': 32, 'П': 33, 'ц': 34, 'С': 35, 'Н': 36, 'К': 37, 'О': 38, '!': 39, 'Т': 40, 'Д': 41, 'З': 42, 'щ': 43, 'Л': 44, 'М': 45, 'У': 46, 'И': 47, 'Б': 48, 'Г': 49, 'Х': 50, 'э': 51, '?': 52, 'Р': 53, 'А': 54, 'Ч': 55, '…': 56, '–': 57, 'ф': 58, ':': 59, 'Я': 60, 'Ц': 61, 'Ж': 62, 'Ш': 63, 'Ф': 64, 'Э': 65, 'Е': 66, 'ё': 67, '_': 68, 'Ю': 69, 'ъ': 70}
idx_to_char = {
    0: ' ', 1: 'о', 2: 'е', 3: '\n', 4: 'а', 5: 'и', 6: 'н', 7: 'т', 8: 'л', 9: 'с', 10: 'р', 11: 'в', 12: '.', 13: 'к', 14: 'у', 15: 'д', 16: 'м', 17: 'п', 18: 'ы', 19: 'я', 20: 'ь', 21: 'й', 22: 'г', 23: 'з', 24: 'б', 25: 'ч', 26: ',', 27: 'х', 28: 'ш', 29: 'ж', 30: 'В', 31: '-', 32: 'ю', 33: 'П', 34: 'ц', 35: 'С', 36: 'Н', 37: 'К', 38: 'О', 39: '!', 40: 'Т', 41: 'Д', 42: 'З', 43: 'щ', 44: 'Л', 45: 'М', 46: 'У', 47: 'И', 48: 'Б', 49: 'Г', 50: 'Х', 51: 'э', 52: '?', 53: 'Р', 54: 'А', 55: 'Ч', 56: '…', 57: '–', 58: 'ф', 59: ':', 60: 'Я', 61: 'Ц', 62: 'Ж', 63: 'Ш', 64: 'Ф', 65: 'Э', 66: 'Е', 67: 'ё', 68: '_', 69: 'Ю', 70: 'ъ'}


class TextRNN(nn.Module):

    def __init__(self, input_size, hidden_size, embedding_size, n_layers=1):
        super(TextRNN, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.embedding_size = embedding_size
        self.n_layers = n_layers

        self.encoder = nn.Embedding(self.input_size, self.embedding_size)
        self.lstm = nn.LSTM(self.embedding_size,
                            self.hidden_size, self.n_layers)
        self.dropout = nn.Dropout(0.2)
        self.fc = nn.Linear(self.hidden_size, self.input_size)

    def forward(self, x, hidden):
        x = self.encoder(x).squeeze(2)
        out, (ht1, ct1) = self.lstm(x, hidden)
        out = self.dropout(out)
        x = self.fc(out)
        return x, (ht1, ct1)

    def init_hidden(self, batch_size=1):
        return (torch.zeros(self.n_layers, batch_size,
                            self.hidden_size, requires_grad=True).to(device),
                torch.zeros(self.n_layers, batch_size,
                            self.hidden_size, requires_grad=True).to(device))


def evaluate(model, char_to_idx, idx_to_char, start_text=' ',
             prediction_len=200, temp=0.3):
    hidden = model.init_hidden()
    idx_input = [char_to_idx[char] for char in start_text]
    train = torch.LongTensor(idx_input).view(-1, 1, 1).to(device)
    predicted_text = start_text

    _, hidden = model(train, hidden)

    inp = train[-1].view(-1, 1, 1)

    for _ in range(prediction_len):
        output, hidden = model(inp.to(device), hidden)
        output_logits = output.cpu().data.view(-1)
        p_next = F.softmax(output_logits / temp, dim=-
                           1).detach().cpu().data.numpy()
        top_index = np.random.choice(len(char_to_idx), p=p_next)
        inp = torch.LongTensor([top_index]).view(-1, 1, 1).to(device)
        predicted_char = idx_to_char[top_index]
        predicted_text += predicted_char

    return predicted_text


device = (
    torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
)


model = TextRNN(input_size=len(idx_to_char), hidden_size=256,
                embedding_size=128, n_layers=2)
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2, amsgrad=True)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    patience=5,
    verbose=True,
    factor=0.45
)


model.load_state_dict(torch.load('nn/hnet'))


def haiku(seed):
    logging.info(f'Generate haiku')
    seed = seed if seed in [*idx_to_char.values()] else ' '
    model.eval()
    return evaluate(model, char_to_idx, idx_to_char,
                    temp=0.3, prediction_len=128,
                    start_text=seed)
