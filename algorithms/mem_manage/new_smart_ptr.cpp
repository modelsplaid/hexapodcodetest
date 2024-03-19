#include<vector>
#include<string>
#include<iostream>
using namespace std;

void test_copy_vector(){
    vector<string> s2;
    {
    vector<string> s1 = {"a","an","the"};
    s2=s1;
    s1[0]="the";
    }
    for(vector<string>::iterator itr=s2.begin();itr<s2.end();itr++){
        cout<<"*itr: "<<*itr<<endl;
    }
    //s2.erase(s2.begin());
    s2.erase(s2.end()-2);
    for(vector<string>::iterator itr=s2.begin();itr<s2.end();itr++){
        cout<<"erase: *itr: "<<*itr<<endl;
    }

    // for(vector<string>::iterator itr=s1.begin();itr<s1.end();itr++){
    //     cout<<"*itr: "<<*itr<<endl;
    // }
    
}


void test_smart_prt(){
    shared_ptr<string> p1=make_shared<string>("hi");

    //*p1="hi";
    
    for(auto itr=p1->begin();itr<p1->end();itr++){
        printf("%c",*itr);

    }
    //cout<<"p1: "<<*p1<<endl;

}


int main(){
    //test_copy_vector();
    test_smart_prt();



    return 0;
}
