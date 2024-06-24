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

def plot_2(x=[1,2,3],y=[[4,5,6],[5,6,7]],legend=["line1","line2"],titlet="figure template"):
    
    for i in range(len(legend)):
        # Plot the first line
        plt.plot(x, y[i], "*")  # The label is used for the legend
        plt.plot(x, y[i],label=legend[i]) 
    
    # Add a legend to the plot
    plt.title(titlet)
    plt.legend()
    # Show the plot
    plt.show()

def plot_1(x=[1,2,3],y=[[4,5,6]],legend=["line1"],titlet="figure template"):
    
    for i in range(len(legend)):
        # Plot the first line
        plt.plot(x, y[i], "*")  # The label is used for the legend
        plt.plot(x, y[i],label=legend[i]) 
    
    # Add a legend to the plot
    plt.title(titlet)
    plt.legend()
    # Show the plot
    plt.show()


def plot_vllm():
    # # plot different head size 
    # legends=["x:head size y: kernel running time(us)"]
    # hd_sz_lst   = [64, 80, 96, 112, 128]
    # time_us_lst = [[287,365,298,575,428]]
    # title1 = "paged attention v2 kernel speed(us) on different head sizes"
    # plot_1(hd_sz_lst,time_us_lst,legends,title1)
    
    # plot different batch size 
    legends=["x:batch size y: kernel running time(us)"]
    batch_sz_lst= [8, 12, 16, 24, 32,48,64,128]
    time_us_lst = [[295,428,562,835,1099,1629,2164,4293]]
    title1 = "paged attention v2 kernel speed(us) on different batch sizes"
    plot_1(batch_sz_lst,time_us_lst,legends,title1)


def plot_attn():
    seq_len  =[512  , 1000  ,2000  ,  4000 ,   8000, 16000 ]
    official =[132  ,153 ,162, 171 , 175,  176]
    shenzhou =[91   ,130 ,144, 152, 154, 155]
    
    plot_2(seq_len,[official,shenzhou],["official","shenzhou"],"Flash Attention throughput(TFLOPS)")

def plot_attn2():
    seq_len  =[1,4,8,16,32,64]
    # v200 =[ 83 ,   84, 142,    212,     340,     658]
    # v258 = [  41,   48,   79,   233,     368,     706]
    # vllm=[ 45 ,   62, 108,    194,     334,     661]
    
    v200 =[ 86 ,   87,  89,    153,     241,     441     ]
    v258 = [  60,   60,  64,     112,    247,      442     ]
    vllm=[  45,   50,   61,    108,     193,      342]
    
    plot_3(seq_len,[v200,v258,vllm],["v200","v258","vllm"],"FlashAtten,VLLM PagedAtten kernel time (us)")


def plot_kskernel():
    batch_sz  =[1,4, 8, 16,32,64]
    vllmpd    =[43,    71,  107,    182,    331,     624]
    dspd      =[65,    82,   120,    175,    320,    582]
    
    plot_2(batch_sz,[vllmpd,dspd],["vllm kernel","deepspeed kernel"],"Kernel runtime(us)")

def plot_ds_prefilldecode():
    batch_sz       = [1,2,4,6,8,12,16, 24,32,64]
    
    prefill        = [ 74,   134,   205,  270,    347,    498,    649,    944,   1238,   2423]
    decode         = [ 53,   55 ,    83,   87,    127,    157,    201,    298,    371,    713]
    prefill_decode = [ 91,  144 ,   241,  332,    420,    606,    788,    1154,  1523,   2993]
    
    plot_3(batch_sz,[prefill,decode,prefill_decode],["prefill","decode","prefill_decode"],"Deepspeed attention kernel run time (us)")

def plot_ds_prefilldecode2():
    import numpy as np
    
    batch_sz       = np.array([1,2,4,6,8,12,16, 24,32,64])
    
    prefill        = np.array([ 74,  134,   205,  270,    347,    498,    649,    944,   1238,   2423])
    decode         = np.array([ 53,  55 ,    83,   87,    127,    157,    201,    298,    371,    713])
    prefill_decode = np.array([ 91,  144,   241,  332,    420,    606,    788,    1154,  1523,   2993])
    print("prefill+decode: ",prefill+decode)
    #plot_2(batch_sz,[prefill_decode,prefill+decode],["combined prefill+decode","seperated prefill+decode"],"Kernel runtime(us)")
  
if __name__ == "__main__":
    #plot_attn()
    #plot_vllm()
    #plot_attn2()
    #plot_kskernel()
    #plot_ds_prefilldecode()
    plot_ds_prefilldecode2()
    

class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode *pre , *rightNode,*prehead;
        prehead = new ListNode(0);
        prehead->next = head;

        // assign left rht ptr
        ListNode *tmp=prehead;
        for(int i=0;i<=right;i++){
            if(i == left-1){
                pre  = tmp;
            }
            if(i==right){
                rightNode = tmp;
            }
            tmp=tmp->next;
        }
        return prehead->next;
    }
};