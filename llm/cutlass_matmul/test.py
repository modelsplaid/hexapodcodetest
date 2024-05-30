#ref: https://medium.com/@aleozlx/cutlass-matrix-multiplication-learning-cutlass-part-ii-41ad00d00e3b

import numpy as np
import time
np.random.seed(123)

def npdot():
    A = np.random.randint(1500, size=30*50).reshape(30, 50)
    #print("A =\n", A)

    B = np.random.randint(2000, size=50*40).reshape(50, 40)
    #print("B =\n", B)

    t1 = time.time()
    C = np.dot(A, B)
    t2 = time.time()
    #print("C =\n", C)
    
    #naieve app
    C = np.empty((30, 40), dtype=int)

    t3 = time.time()
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            C[i, j] = np.dot(A[i, :], B[:, j])
    t4 = time.time()     
    
    #print("C =\n", C)
    
    #cache friendly matmul
    C = np.zeros((30, 40), dtype=int)
    
    t5 = time.time()
    for k in range(A.shape[1]):
        C += np.outer(A[:, k], B[k, :])
    t6 = time.time()
    
    print("np time: ",(t2-t1)*1000,"naieve time: ", (t4-t3)*1000,"cach friend time: ",(t6-t5)*1000) 
    
def npdot_even_cache_friend():
    # Now optimize matrix storing by treating C as a block matrix. 
    # Suppose we will write C[:, 0:2] first then C[:, 2:4], and pretend this is the block size (3, 2) 
    # that will fit entirely on the device.
    
    A = np.random.randint(15, size=3*5).reshape(3, 5)
    print("A =\n", A)

    B = np.random.randint(20, size=5*4).reshape(5, 4)
    print("B =\n", B)
    
    C = np.zeros((3, 4), dtype=int)
    block_size = (3, 2)
    div_up = lambda a, b: (a + b - 1) // b

    
    ### CUDA Grid
    for m in range(0, C.shape[0], block_size[0]):
        print("m: ",m,"C.shape[0]: ",C.shape[0]," block_size[0]: ",block_size[0])
        
        for n in range(0, C.shape[1], block_size[1]): 
            print("n: ",n,"C.shape[1]: ",C.shape[1],"block_size[1]: ",block_size[1])
            ### Main loop in the CUDA kernel
            ### Smaller K is favorable to satisfy the shared memory bandwidth
            for k in range(A.shape[1]):

                ### The 3x2 block is what hypothetically fits in the shared memory.
                ### The thread block will contain multiple warps.
                row_range = slice(m, m+block_size[0])
                col_range = slice(n, n+block_size[1])

                ### Each warp loads a "fragment" into the register file
                ### from the shared memory. Here we didn't show warp-level
                ### decomposition, but it's essentially an unrolled loop
                ### that further divides the {row,col}_range
                frag_A = A[row_range, k]
                frag_B = B[k, col_range]

                ### Warp threads cooperatively compute the outer product.
                ### This can be done using a warp-level primitive "WMMA" since CUDA 9.
                ### nvcuda::wmma can be used to target the CUDA Tensor Cores
                
                #print("frag_A: ",frag_A)
                #print("frag_B: ",frag_B)
                C[row_range, col_range] += np.outer(frag_A, frag_B)
                print(C)
            print(f"C(t={n//block_size[1]}) =\n", C)

if __name__=="__main__":
    npdot_even_cache_friend()
    #npdot()