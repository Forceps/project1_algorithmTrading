import torch.nn as nn
import torch.nn.functional as F


class SharingNetwork(nn.Module):
    def __init__(self, input_size: int = 1401, dropout_ratio: float = 0.5):
        super(SharingNetwork, self).__init__()

        self.dropout_ratio = dropout_ratio

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=180, num_layers=1)

    def __call__(self, x):

        output, _ = self.lstm(x)
        y = F.dropout(output, p=self.dropout_ratio)

        return y

