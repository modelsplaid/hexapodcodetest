import matplotlib.pyplot as plt

def plot_3(x=[1,2,3],y=[[4,5,6],[5,6,7],[7,8,9]],legend=["line1","line2","line3"],titlet="figure template"):
    
    for i in range(len(legend)):
        # Plot the first line
        plt.plot(x, y[i], "*")  # The label is used for the legend
        plt.plot(x, y[i],label=legend[i]) 
    
    # Add a legend to the plot
    plt.title(titlet)
    plt.legend()
    # Show the plot
    plt.show()

if __name__ == "__main__":
    legends=["flash attn v1","flash attn v2","flash attn v2.5.7"]
    batch_lst          = [16  ,32   ,64   ,128,256, 512   ,1024 ]
    time_ms_batch_v123 = [[1.07,1.94,3.88,7.33,14.2,28.46,57.07],
                          [0.81,1.09,2.16,4.35,8.76,17.54,35.26],
                          [0.68,1.35,2.27,4.45,8.97,17.94,35.94]]
    title1 = "Kernel speed(ms) on different batches"
    
    seqlen_lst         = [1024,1536,2048,3072,4096 ,6144 ,8192   ]
    time_ms_seq_v123   = [[3.81 ,8.57 ,15.12,33.47,59.46,134.11,242.53],
                          [2.21 ,4.89,8.61  ,18.88,36.91 ,116.92 ,133.94],
                          [2.75 ,4.76,8.41  ,18.66,32.92 ,73.70 ,131.00]]
    title2 = "Kernel speed(ms) on different sequence lenth"
    
    plot_3(batch_lst,time_ms_batch_v123,legends,title1)
    plot_3(seqlen_lst,time_ms_seq_v123,legends,title2)