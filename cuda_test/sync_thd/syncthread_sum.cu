#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <iostream>

#define TILE_SIZE 16  // Assuming each block processes a tile of 16 elements

// Reduction kernel to compute the sum of elements in a tile
__global__ void reduceKernel(int *input, int *output, int N) {
    extern __shared__ float sdata[];

    // Each thread loads a unique element from the input array
    unsigned int tid = threadIdx.x;
    unsigned int i = blockIdx.x * TILE_SIZE + threadIdx.x;

    // Load the element into shared memory
    if (i < N) {
        sdata[tid] = input[i];
    } else {
        sdata[tid] = 0;  // Guard against out-of-bounds access
    }

    // Wait for all threads to load their data
    __syncthreads();

    // Do reduction in shared memory
    for (unsigned int s = TILE_SIZE / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        // Wait for all threads to perform the addition
        __syncthreads();
    }

    // The first thread writes the result to the output array
    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}

int main() {
    int N = 1024;  // Total number of elements
    int *h_input = new int[N];  // Host input array
    h_input[0]=5;
    h_input[1]=6;
    h_input[2]=7;
    float *h_output = new float[N / TILE_SIZE];  // Host output array for block sums

    // Initialize host input array and allocate device memory
    int *d_input, *d_output;
    cudaMalloc(&d_input, N * sizeof(int));
    cudaMalloc(&d_output, (N / TILE_SIZE) * sizeof(float));

    // Copy input data from host to device
    cudaMemcpy(d_input, h_input, N * sizeof(int), cudaMemcpyHostToDevice);

    // Launch the kernel
    reduceKernel<<<N / TILE_SIZE, TILE_SIZE>>>(d_input, d_output, N);

    // Check for and handle errors here

    // Copy the result back to host memory
    cudaMemcpy(h_output, d_output, (N / TILE_SIZE) * sizeof(float), cudaMemcpyDeviceToHost);

    // Compute the final result by summing the block sums on the host
    float totalSum = 0;
    for (int i = 0; i < N / TILE_SIZE; ++i) {
        totalSum += h_output[i];
    }

    // Cleanup memory
    cudaFree(d_input);
    cudaFree(d_output);
    delete[] h_input;
    delete[] h_output;

    // Print the result
    printf("Total sum: %f\n", totalSum);

    return 0;
}
