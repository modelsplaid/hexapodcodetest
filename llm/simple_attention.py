import torch
import torch.nn.functional as F

# Assume query, key, and value are tensors with appropriate shapes
query = torch.randn(1, 1, d_k)  # (num_queries, 1, d_k)
key = torch.randn(1, d_k, 1)   # (1, d_k, num_keys)

# Compute attention scores
scores = torch.matmul(query, key.transpose(-2, -1))  # (num_queries, 1, num_keys)

# Apply softmax to the scores across the keys dimension
attention_weights = F.softmax(scores, dim=-1)  # (num_queries, 1, num_keys)

# Now, attention_weights can be used to weight the value vectors
value = torch.randn(1, d_v, 1)  # (1, d_v, num_values)
weighted_value = torch.matmul(attention_weights, value)  # Weighted sum of values