batch=32
seq=512
nheads=32
headdim=128
layer=32                                  
atten_size = 4*batch*(seq)*nheads*headdim*layer/1000000000
print("atten_size: ",atten_size)
