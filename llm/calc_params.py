import torch
from torch import nn

# https://discuss.pytorch.org/t/how-do-i-check-the-number-of-parameters-of-a-model/4325/9
def count_parameters(model: torch.nn.Module) -> int:
    """ Returns the number of learnable parameters for a PyTorch model """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def test_atten():
    d_model = 512
    n_heads = 8  # must be a divisor of `d_model`

    multi_head_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=n_heads)
    print(count_parameters(multi_head_attention))  # 1050624
    print(4 * (d_model * d_model + d_model))  # 1050624


class TransformerFeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super(TransformerFeedForward, self).__init__()
        self.d_model = d_model
        self.d_ff = d_ff

        self.linear1 = nn.Linear(self.d_model, self.d_ff)
        self.relu = nn.ReLU()
        self.linear2 = nn.Linear(self.d_ff, self.d_model)

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x

def calc_feedfwd():
    # ffn = max(0,xW1+b1)W2+b2
    
    d_model = 512
    d_ff = 2048

    feed_forward = TransformerFeedForward(d_model, d_ff)
    print(count_parameters(feed_forward))  # 2099712
    print(2 * d_model * d_ff + d_model + d_ff)  # 2099712
    
if __name__ == '__main__':
    calc_feedfwd()