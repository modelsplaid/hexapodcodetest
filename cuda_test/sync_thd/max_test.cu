#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <iostream>

using namespace std;


__device__ void exampleKernel2() {
    // Example values
    float a = 50.0f;
    float b = 100.0f;

    // Compute the maximum of a and b
    float max_value = max(a, b);

    printf("max %f  threadIdxx: %d threadIdxy: %d blockIdxx: %d blockIdxy: %d \n",
          max_value,threadIdx.x,threadIdx.y,blockIdx.x,blockIdx.y);
    // Use max_value for further computation...
}

__global__ void exampleKernel() {
    // Example values
    float a = 5.0f;
    float b = 10.0f;

    // Compute the maximum of a and b
    float max_value = max(a, b);
    printf("blockDim.x: %d blockDim.y: %d gridDim.x: %d gridDim.y: %d \n",
            blockDim.x,blockDim.y,gridDim.x,gridDim.y);
    printf("max %f  threadIdxx: %d threadIdxy: %d blockIdxx: %d blockIdxy: %d \n",
          max_value,threadIdx.x,threadIdx.y,blockIdx.x,blockIdx.y);
    
    //exampleKernel2();
    
    __syncthreads();  // such that the inner loop can use the correct Kj, Vj

    // Use max_value for further computation...
}

int main() {
    dim3 grid_dim(1,1);  // batch_size x num_heads
    dim3 block_dim(2,2);  // Bc threads per block
    const int sram_size =1000;
    exampleKernel<<<grid_dim, block_dim,sram_size>>>();

    cudaDeviceSynchronize(); // Ensure the kernel has completed
    return 0;
}
