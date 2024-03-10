from transformers import AutoModel
from torch import nn


class LCModel(nn.Module):
    def __init__(self, layers=[], device=None) -> None:  # fix this
        """
        layers: list of layer sizes
        device: device to run model on
        """

        super().__init__()

        self.device = device
        self.input_size = layers[0]
        self.output_size = layers[-1]
        self.num_layers = len(layers)

        self.layer_list = nn.ModuleList()
        for i in range(self.num_layers - 1):
            self.layer_list.append(nn.Linear(layers[i], layers[i + 1]))
            self.layer_list.append(nn.ReLU())
        self.layer_list.append(nn.Sigmoid())

    def forward(self, x):
        for layer in self.layer_list:
            x = layer(x)
        return x