#include<map>
#include<set>
#include<iostream>
#include<queue>
using namespace std;

void test_map(){
    map<string,int> nam_count;
    string word;
    while(true){
        cout<<"input: ";cin>>word;
        if(word=="q"){
            cout<<"done"<<endl;
            break;
        }else{

            nam_count[word]=nam_count[word]+1;
        }

        for(map<string,int>::iterator itr=nam_count.begin();itr!=nam_count.end();itr++){
            cout<<"name: "<<itr->first<<" count: "<<itr->second<<endl;
        }
    }

}


void test_map_set(){
    map<string,int> nam_count;
    set<string> rm_set;
    rm_set.emplace("the");
    rm_set.emplace("to");
    for(set<string>::iterator itr=rm_set.begin();itr!=rm_set.end();itr++){
        cout<<"set: "<<*itr<<endl;
    }

    set<string>::iterator fd=rm_set.find("the");
    cout<<"fd==end: "<< bool(fd==rm_set.end())<<endl;
    cout<<"fd: "<<*fd<<endl;
    string word;
    while(true){
        cout<<"input: ";cin>>word;

        if(word=="q"){
            cout<<"done"<<endl;
            break;
        }else{
            
            if(rm_set.find(word)!=rm_set.end()){
                cout<<"skip: "<<word<<endl;
                continue;

            }
            nam_count[word]=nam_count[word]+1;
        }
        
        for(map<string,int>::iterator itr=nam_count.begin();itr!=nam_count.end();itr++){
            cout<<"name: "<<itr->first<<" count: "<<itr->second<<endl;
        }
    }
}

void test_pair(){
    pair<string,string> ssp;
    ssp.first="hi";
    ssp.second="world";
    cout<<"pair: "<<ssp.first<<ssp.second<<endl;

}

void test_multi_sets(){
    vector<int> ivec;
    for(auto i=10;i>0;i--){
        ivec.push_back(i);
        ivec.push_back(i);
    }

    for(vector<int>::iterator itr=ivec.begin();itr<ivec.end();itr++){
        cout<<"ivec: "<<*itr<<endl;
    }

    set<int> iset(ivec.begin(),ivec.end());
    for(set<int>::iterator itr=iset.begin();itr!=iset.end();itr++){
        cout<<"iset: "<<*itr<<endl;
    }

    //multiset<int,less<int>> mset(ivec.begin(),ivec.end());
    multiset<int,greater<int>> mset(ivec.begin(),ivec.end());
    for(set<int>::iterator itr=mset.begin();itr!=mset.end();itr++){
        cout<<"mset: "<<*itr<<endl;
    }

    // for(set<int>::iterator itr=--mset.end();itr!=--mset.begin();itr--){
    //     cout<<"ascend mset: "<<*itr<<endl;
    // }

}

void test_priority_q(){

    priority_queue< int, vector<int>, greater<int> > pq;
    pq.push(12);
    pq.push(24);
    pq.push(12);
    pq.push(3);
    pq.push(24);
    cout << "priority_queue (using vector) listing" << endl;
    while(!pq.empty())
    {
        cout << pq.top() << endl;
        pq.pop();
    }
}
int main(){
    //test_map();
    //test_map_set();
    //test_pair();
    //test_multi_sets();
    test_priority_q();

}
