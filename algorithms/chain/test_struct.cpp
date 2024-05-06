#include <string>
#include <iostream>

struct ListNode{
    int val;
    ListNode *next;
    ListNode(int x): val(x){}
    ListNode(int x, ListNode *next): val(x),next(next){}
};

using namespace std;
int main(void){
    ListNode ln(3);
    cout<<"val: "<<ln.val<<endl;



}

