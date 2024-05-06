#include<unordered_map>
#include<iostream>
#include<vector>

using namespace std;
void test1(){
    std::unordered_map<std::string,std::string> cor={{"red","yes"},{"black","no"}};
    std::vector<int> a={1,2,3};
    for (auto one:a){
        std::cout<<"a: "<<one<<std::endl;
    }

    for (auto one_clr:cor){
        auto fst=one_clr.first;
        auto scnd=one_clr.first;
        std::cout<<"fst: "<<fst<<" scnd"<<scnd<<std::endl;
        //std::cout<<"one_clr: "<<red;
    } 

    for (auto&& [first, second] : cor)
    {
        std::cout<<"first:"<<first<<" second:"<<second<<std::endl;
    }

    auto fst_fnd=cor.find("red");

    std::cout<<"fnd red: "<<fst_fnd->first<<fst_fnd->second<<std::endl;

    auto ab=fst_fnd->first; 

    unordered_map<string,string>::iterator itr;

    itr = cor.find("yellor");
    if(itr==cor.end()){
        cout<<"cannot find"<<endl;
    }else{
        cout<<"yellor: "<<itr->first<<endl;
    }

}

void test_un_map(){
    unordered_map<int,int> um;
    um[3]=6;
    um[7]=8;
    
    unordered_map<int,int>::iterator it= um.find(5);
    if(it==um.end()){
        cout<<"no"<<endl;
    }

    unordered_map<int,int>::iterator it2= um.find(3);
    if(it2!=um.end()){
        cout<<"fst: "<<it2->first<<"sec: "<<it2->second<<endl;
    }



}

int main(void){

    test_un_map();


}