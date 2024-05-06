#include <iostream>
using namespace std;

class box{
    public:

    box(){
        cout<<"create box"<<endl;
    }

    ~box(){
        cout<<"destroy box"<<endl;
    }

};

int main(){

box* bptr=NULL;

bptr=new box[5];

delete [] bptr;
return 0;
}
