import torch

key_labels = [
    "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
    "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "shift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "ctrl", "space"
]
size = len(key_labels)

def create_one_hot_matrix(size: int) -> torch.Tensor:
    one_hot_matrix = torch.zeros((size, size), dtype=torch.float32)
    for i in range(size):
        one_hot_matrix[i, i] = 1.0
    return one_hot_matrix

print(create_one_hot_matrix(size))

# output:
# tensor([[1., 0., 0.,  ..., 0., 0., 0.],
#         [0., 1., 0.,  ..., 0., 0., 0.],
#         [0., 0., 1.,  ..., 0., 0., 0.],
#         ...,
#         [0., 0., 0.,  ..., 1., 0., 0.],
#         [0., 0., 0.,  ..., 0., 1., 0.],
#         [0., 0., 0.,  ..., 0., 0., 1.]])
