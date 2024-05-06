import torch
import torch.nn.functional as F

def online_softmax(scores, max_length, block_size):
    """
    在线softmax计算的简化实现。
    
    参数:
    - scores: 形状为 (batch_size, seq_length, ...) 的张量，表示原始分数。
    - max_length: 序列的最大长度。
    - block_size: 每个块中将被同时处理的序列元素的数量。
    
    返回:
    - probs: 形状与scores相同，表示softmax后的概率。
    """
    # 初始化输出张量
    probs = torch.zeros_like(scores)
    max_scores = torch.zeros_like(scores[:, :1])  # 存储每个块的最大分数

    for i in range(0, max_length, block_size):
        block = scores[:, i:i+block_size]
        # 计算当前块的softmax分数
        exp_block = torch.exp(block - max_scores[:, :1].expand_as(block))
        # 累积softmax分数
        probs[:, i:i+block_size] = exp_block / (exp_block.sum(dim=-1, keepdim=True) + 1e-9)
    
    # 返回累积的softmax概率
    return probs

# 示例使用
batch_size, seq_length, feature_dim = 2, 50, 64
scores = torch.randn(batch_size, seq_length, feature_dim)

# 使用在线softmax计算
block_size = 10
probs = online_softmax(scores, seq_length, block_size)

print(probs)
