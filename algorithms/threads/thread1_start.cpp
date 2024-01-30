//https://baptiste-wicht.com/posts/2012/03/cpp11-concurrency-part1-start-threads.html
#include<iostream>
#include<thread>
#include<unistd.h>

using namespace std;

void thd1(){
    cout<<"thread id: "<<std::this_thread::get_id()<<endl;
    cout<<"running thd1"<<endl;
    sleep(1);
    cout<<"running thd2"<<endl;
    usleep(1000);
    cout<<"running thd3"<<endl;

}

int main(){

    thread t1(thd1);
    thread t2(thd1);
    cout<<"start join";
    t1.join();
    cout<<"joind t1";
    t2.join();
    cout<<"joind t2";
    //t1.detach();
    sleep(1);
    usleep(2000);

    int arr[5]={1,2,3,4,0};

    try{

        
        for(auto a:arr){
            cout<<"a: "<<1/a<<endl;
        }

    }catch(std::exception& e){
        cout<<"catched err: "<<endl;
    }

    cout<<"main id: "<<this_thread::get_id()<<endl;
    
}
