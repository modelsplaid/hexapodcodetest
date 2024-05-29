#bench mark: https://pytorch.org/tutorials/recipes/recipes/benchmark.html
import torch.utils.benchmark as benchmark
import torch


def batched_dot_mul_sum(a, b):
    '''Computes batched dot by multiplying and summing'''
    return a.mul(b).sum(-1)


def batched_dot_bmm(a, b):
    '''Computes batched dot by reducing to ``bmm``'''
    a = a.reshape(-1, 1, a.shape[-1])
    b = b.reshape(-1, b.shape[-1], 1)
    return torch.bmm(a, b).flatten(-3)


# Input for benchmarking
x = torch.randn(10000, 64,device='cuda')
y1 = torch.randn(10000, 64,device='cuda')

# Ensure that both functions compute the same output
#assert batched_dot_mul_sum(x, x).allclose(batched_dot_bmm(x, x))
batched_dot_mul_sum(x, y1)

num_threads = torch.get_num_threads()
print(f'Benchmarking on {num_threads} threads')

t0 = benchmark.Timer(
    stmt='batched_dot_mul_sum(x, y)',
    setup='from __main__ import batched_dot_mul_sum',
    globals={'x': x,'y':y1},num_threads=num_threads)
    

t1 = benchmark.Timer(
    stmt='batched_dot_bmm(x, z)',
    setup='from __main__ import batched_dot_bmm',
    globals={'x': x,'z':y1},num_threads=num_threads)

print(t0.timeit(10000))
print(t1.timeit(10000))