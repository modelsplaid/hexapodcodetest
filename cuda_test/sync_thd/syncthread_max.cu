#include <cuda_runtime.h>

__global__ void reduceKernel(int *input, float *output) {
    extern __shared__ float sdata[];

    // Each thread loads one element from global memory to shared memory
    unsigned int tid = threadIdx.x;
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
    sdata[tid] = input[i];

    // Wait for all threads to load their data
    __syncthreads();

    // Perform reduction to find the maximum value in the shared memory block
    for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            float a = sdata[tid];
            float b = sdata[tid + s];
            sdata[tid] = (a > b) ? a : b;
        }
        // Wait for all threads to complete the reduction step
        __syncthreads();
    }

    // The first thread in the block stores the block result in global memory
    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}

int main() {
    // Assume 'h_input' and 'h_output' are appropriately sized host arrays
    int *h_input, *h_output;
    // ... code to allocate and initialize 'h_input' and 'h_output' ...

    int *d_input, d_output;
    // ... code to allocate device memory for 'd_input' and 'd_output' ...

    // Copy data from host to device memory
    cudaMemcpy(d_input, h_input, ..., cudaMemcpyHostToDevice);

    // Invoke the kernel
    reduceKernel<<<N, M>>>(d_input, d_output);

    // Copy the result back to host memory
    cudaMemcpy(h_output, d_output, ..., cudaMemcpyDeviceToHost);

    // ... rest of the code ...

    return 0;
}
