#include<iostream>
#include<unordered_set>

using namespace std;

int main(){
    unordered_set<int> uns;
    uns.insert(5);
    uns.insert(5);
    uns.emplace(6);
    uns.emplace(7);
    uns.emplace(7);
    for(auto one_u:uns){
        cout<<"one_uns: "<<one_u<<endl;
    }

    cout<<"cout(5): "<<uns.count(5)<<endl;

    auto iter=uns.find(9);
    if(iter!=uns.end()){
        cout<<"now found: "<<*iter<<"\n";
    }else{
        cout<<"cannot find(9) \n";
    }


    // if(iter==uns.end()){
    //     cout<<"found: "<<*iter<<"\n";
    // }else{

    //     cout<<"not found \n";
    // }

    for(unordered_set<int>::iterator iter=uns.begin();iter!=uns.end();iter++){
        if(*iter == 5){
            
            cout<<"iter found 5 \n" ;

            
        }
        
         cout<<"iter:"<<*iter<<endl;
    }

    return 0;
}