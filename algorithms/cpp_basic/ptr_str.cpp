#include<iostream>
using namespace std;

int main(){
    char spl[]="hello";
    spl[0]='H';

    char *spt="world";
    spt[0]='W';
    cout<<"spl: "<<spl<<endl;
    return 0;

}
