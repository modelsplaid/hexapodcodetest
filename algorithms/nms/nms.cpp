#include<iostream>
#include<algorithm>
#include<vector>

using namespace std;

void print_vecf(vector<float> &c){

    cout<<"vec val: ";
    for(vector<float>::iterator itr=c.begin();itr<c.end();itr++ ){
        cout<< *itr<<" ";
    }
    cout<<endl;
}

void print_boxes(vector<vector<float>> &c){
    for(vector<vector<float>>::iterator itr=c.begin();itr<c.end();itr++){
        print_vecf(*itr);

    }
}

float iou(vector<float> &A,vector<float> &B){
    // left_top_x left_top_y right_btn_x riht_btn_y
    //  0            1           2           3 
    auto area_a= (A[3]-A[1])*(A[2]-A[0]);
    auto area_b= (B[3]-B[1])*(B[2]-B[0]);

    auto inter_h =  max(0,int(min(B[3],A[3])-max(B[1],A[1])));
    auto inter_w =  max(0,int(min(B[2],A[2])-max(B[0],A[0])));
    //cout<<"inter h: "<< inter_h<<"inter_w: "<<inter_w<<endl;
    auto inter_area = inter_h*inter_w;

    float iou = inter_area/(area_a+area_b-inter_area);
    cout<<"iou: "<<iou<<endl;
    return iou;

}

void test_iou(){
    auto a=max(10,9);
    vector<float> A={0,0,5,5};
    vector<float> B={0,0,5,10};

    iou(A,B);
    // vector<float>::iterator
    // cout<<"a: "<<a<<endl;

}

int nms(vector<vector<float>> &boxes,float thresh){
    // tood: here

}

int main(){
    vector<vector<float>> boxes={{0, 0, 100, 101, 0.9}, 
                                  {5, 6, 90, 110, 0.7}, 
                                  {17, 19, 80, 120, 0.8}, 
                                  {10, 8, 115, 105, 0.5}};

    print_boxes(boxes);

    //nms(boxes,thresh);
}