#include<iostream>
#include<string>
#include<array>
using namespace std;


void test_const(){
    const int v2=0;
    int v1=v2;
    int *p1=&v1,&r1=v1;
    int i=0;
    const int *p2=&v2,*const p3=&i;

    const int *const p4=p3;
    r1=v2;
    p2=p1;
    //*p2=3; //error: read-only variable is not assignable
    //p3=p2;//variable 'p3' declared const here
    p2=p3;

}

void test_string(){
    string a="world";
    a="hello";
    cout<<a<<",sz:"<<a.size()<<endl;

    for(string::iterator it=a.begin();it<=a.end();it++){
        cout<<"it: "<<*it<<endl;
    }

    // char* cp = "Hello World!";
    // string str(cp+6,6);
    // for(string::iterator it=str.begin();it<str.end();it++){
    //     cout<<"itcp: "<<*it<<endl;
    // }

}

void test_vector(){

    vector<vector<int>> vvi;
    //vector<string> a(10);
    vector<int> a(2);
    //for (vector<int>::iterator it=a.begin();it<=a.end();it++){
    for (auto it=a.begin();it<=a.end();it++){    
        cout<<"a_it:"<<*it<<endl;
    }
    a.reserve(100);
    cout<<"a.capacity: "<<a.capacity()<<endl;

    // test copy
    auto b=a;
    b[3]=5;
    cout<<"b3: "<<b[3]<<" a[3]"<<a[3]<<endl;

    b.insert(b.begin()+1,34);

    for(auto it=b.begin();it<b.end();it++){
        cout<<"b after insert: "<<*it<<endl;
    }

    vector<string> svec;
    svec.insert(svec.begin(),3,"hello");
    for(auto itr=svec.begin();itr<svec.end();itr++){
        //cout<<"svec: "<<*itr<<endl;
    }
    string str1="first edit";
    svec.emplace(svec.end(),str1);
    str1="second edit";
    for(auto iter=svec.begin();iter<svec.end();iter++){
        cout<<"svec2: "<<*iter<<endl;
    }

    auto &&lst=svec.back();
    auto lst1=svec.back();

    cout<<"&&lst: "<<lst<<endl;
    cout<<"lst1: "<<lst1<<endl;



    
    
}

void array_test(){
    array<int,5> c;
    c[2]=3;
    cout<<"c5:"<<c[5]<<endl;
    for (array<int,5>::iterator it=c.begin();it<=c.end();it++){
        cout<<"c:"<<*it<<endl;
    }
}

int main(){
    //test_string();
    test_vector();
    //array_test();

}