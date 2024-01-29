#include<stack>
#include<iostream>
#include<vector>
using namespace std;

void tstack(){
    stack<int> stk;
    //stk.push(13);
    //stk.push(16);
    //stk.push(19);
    stk.push(19);
    stk.emplace(13);
    stk.emplace(16);
    stk.emplace(19);

    auto sz=stk.size();
    for(auto i=0;i<sz;i++){
        cout<<"stack one: "<<stk.top()<<" size: "<<stk.size() <<endl;
        stk.pop();
    }

    vector<int> vec1={3,4,5}; 
    stack<vector<int>> stk1;

    //stk1.emplace(vec1);
    stk1.push(vec1);
    auto sz1=stk1.size();

     for(auto i=0;i<sz1;i++){
        auto a=stk1.top();
        for(auto one:a){
         cout<<"stk1 one: "<<one<<" size: "<<stk1.size() <<endl;

        }
         stk1.pop();
     }
}

void tvector(){

    vector<int> stk;
    stk.push_back(3);
    stk.push_back(6);
    stk.push_back(9);

    for(auto one:stk){
        cout<<"vector one: "<<one<<endl;
    }
}

void stack_swap(){
    stack<int> stk;
    stk.push(19);
    stk.emplace(13);
    stk.emplace(16);
    stk.emplace(19);

    stack<int> stk1;
    stk1.emplace(130);
    stk1.emplace(160);
    stk1.emplace(190);

    stk.swap(stk1);

    auto sz=stk.size();
    for(auto i=0;i<sz;i++){
        cout<<"stk: "<<stk.top()<<" size: "<<stk.size() <<endl;
        stk.pop();
    }

    auto sz1=stk1.size();
    for(auto i=0;i<sz1;i++){
        cout<<"stk1: "<<stk1.top()<<" size: "<<stk1.size() <<endl;
        stk1.pop();
    }


}

int main(){
    //tvector();
    //tstack();
    stack_swap();

}