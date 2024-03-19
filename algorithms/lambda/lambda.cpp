//https://leetcode.cn/leetbook/read/cmian-shi-tu-po/vwegz6/

#include<iostream>
using namespace std;

void value_params(){
    int a = 10;
    auto f=[a](int b)mutable->float {
        auto c = a+b;
        a=20;
        return c;
    };

    cout<<a<<endl; // 10
    cout<<f(20)<<endl; // 30
    cout<<a<<endl; // 10

}

void value_imp_params(){
    int a = 90;
    auto f=[=](int b)mutable->float {
        auto c = a+b;
        a=100;
        return c;
    };

    cout<<a<<endl; // 90
    cout<<f(20)<<endl; // 110
    cout<<a<<endl; // 90

}


void lmbda(){
    auto f=[](){return 33;};
    cout<<"f:"<<f()<<endl;

}

int main()
{
    // cout<<"test value transfer"<<endl;
    // value_params();

    // cout<<"test value implicit transfer"<<endl;
    // value_imp_params();

    lmbda();
    return 0;
}
