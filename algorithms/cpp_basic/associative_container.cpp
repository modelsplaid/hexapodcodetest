#include<map>
#include<set>
#include<iostream>
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
int main(){
    //test_map();
    test_map_set();

}
