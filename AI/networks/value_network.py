import torch.nn as nn
import torch.nn.functional as F


class ValueNetwork(nn.Module):
    def __init__(self, input_size: int = 170, hidden_size: int = 170, dropout_ratio: float = 0.5):
        super(ValueNetwork, self).__init__()
        self.dropout_ratio = dropout_ratio

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=1, dropout=dropout_ratio)

        self.affine1 = nn.Linear(hidden_size, hidden_size)
        self.affine2 = nn.Linear(hidden_size, 1)

    def __call__(self, x):

        output, _ = self.lstm(x)
        y = F.dropout(output, p=self.dropout_ratio)

        y = F.relu(self.affine1(y))
        y = self.affine2(y)

        return y

