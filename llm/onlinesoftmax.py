import numpy as np
import torch
import torch.nn.functional as F

input_list = [0.2,0.12,0.45,0.05,-0.001,0.1,0.5,0.3]
print(input_list)

input_list_1 = input_list[:4]
input_list_2 = input_list[4:]

print(input_list_1)
print(input_list_2)

d0=0
m0=-np.inf
prev_m=m0
for x in input_list_1:
    m0=max(x,m0)
    d0=d0*np.exp(prev_m-m0)+np.exp(x-m0)
    prev_m=m0

print("m0: ",m0,"d0: ",d0)

d1=0
m1=-np.inf
prev_m=m1
for x in input_list_2:
    m1=max(x,m1)
    d1=d1*np.exp(prev_m-m1)+np.exp(x-m1)
    prev_m=m1

print("m1: ",m1,"d1: ",d1)

o0=[np.exp(x-m0)/d0 for x in input_list_1]
o1=[np.exp(x-m1)/d1 for x in input_list_2]
print("o0: ",o0)
print("o1: ",o1)

# Merge first and second list
real_m = max(m0,m1)
print("real_m: ",real_m)

d_new = np.exp(m0-real_m)*d0+np.exp(m1-real_m)*d1
print("d_new: ",d_new)

o1_new = [i*np.exp(m0-real_m)*d0/d_new for i in o0] 
print("o1_new: ",o1_new)

o2_new = [i*np.exp(m1-real_m)*d1/d_new for i in o1] 
print("o2_new: ",o2_new)

print("sum_o1 new: ",sum(o1_new))
print("sum_o2 new: ",sum(o2_new))
print("sum two; ",sum(o1_new)+sum(o2_new))


