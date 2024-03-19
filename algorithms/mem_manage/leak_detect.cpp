//ref: https://www.osc.edu/resources/getting_started/howto/howto_use_address_sanitizer
//gcc noleak.c -o noleak -fsanitize=address -static-libasan -g

#include<stdlib.h>
#include<string>
#include<iostream>
using namespace std;

void no_leakage(){
    char *ch= (char *)malloc(100);
    strcpy(ch,"hellow world");
    printf("%s\n",ch);
    //cout<<ch<<endl;
    free(ch);
}

void no_free(){
    char *ch= (char *)malloc(100);
    strcpy(ch,"hellow world");
    printf("%s\n",ch);
}

void use_aft_free(){
    char *ch=(char*) malloc(100);
    free(ch);
    strcpy(ch,"hellow world");
    printf("%s\n",ch);
}

void heap_ovflow(){
    char *ch=(char*) malloc(3);
    strcpy(ch,"hellow world");
    printf("%s\n",ch);

}

int main(){

//no_leakage();
//no_free();
//use_aft_free();
heap_ovflow();
return 0;
}
