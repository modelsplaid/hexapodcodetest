#include<deque>
#include<iostream>
using namespace std;


// show dq(dequeue<int> &dq){

    
// }
int main(){

    deque<int> dq;
    dq.emplace_back(1);
    dq.emplace_back(2);
    dq.emplace_front(3);

    //deque<int>::iterator it;
    for(auto it=dq.begin();it!=dq.end();it++){
        cout<<"*it:"<<*it<<endl;

    }



    

}
