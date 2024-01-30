//https://baptiste-wicht.com/posts/2012/03/cpp11-concurrency-part1-start-threads.html
#include<iostream>
#include<thread>
#include<unistd.h>
#include<vector>

using namespace std;

struct counter{
    int a=0;
    void increament(){
        a++;

    }

};

counter one_cntr;

void thd(){
    std::mutex mtx;

    mtx.lock();

    for(int a=0;a<10;a++){
        one_cntr.increament();
    }
    cout<<"a: "<<one_cntr.a<<endl;
    mtx.unlock();


}

int main(){
    vector<thread> thd_vec;
    for(int i=0;i<2;i++){
        thd_vec.push_back(thread(thd));
    }

    for(auto &one:thd_vec){
        one.join();
    }
        cout<<"final a: "<<one_cntr.a<<endl;
}
