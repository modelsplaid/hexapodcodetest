
//Definition for singly-linked list.
#include<iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        
        ListNode* root= new ListNode;
        ListNode* rtroot=root;
        int inc = 0;

        while(l1!=nullptr && l2!=nullptr){
            ListNode* lsum= new ListNode;

            int val = l1->val + l2->val;
            l1=l1->next;
            l2=l2->next;

            int inc1 = val % 10;
            if(val>9){
                int rmder = val-10;
            }    else{

                int rm
            }
            lsum->val = rmder+inc;
            inc = val % 10;

            root->next = lsum;
            root=root->next;

        }

        while(l1 != nullptr){
            ListNode* lsum= new ListNode;
            int val = l1->val+inc;
            l1=l1->next;

            inc =0;

            root->next = lsum;
            root=root->next;

        }

        while(l2 != nullptr){
            ListNode* lsum= new ListNode;
            int val = l2->val+inc;

            l2=l2->next;
            inc =0;

            root->next = lsum;
            root=root->next;
        }

        if (inc!=0){
            ListNode* lsum= new ListNode;
            lsum->val = inc;
            root->next=lsum;
        }

        return rtroot->next;

    }
};

int main(){

ListNode* l11 = new ListNode(2);
ListNode* l12 = new ListNode(4);
ListNode* l13 = new ListNode(3);
l11->next=l12;
l12->next=l13;

ListNode* l21 = new ListNode(5);
ListNode* l22 = new ListNode(6);
ListNode* l23 = new ListNode(4);
l21->next=l22;
l22->next=l23;

Solution sol;
ListNode* l4 = sol.addTwoNumbers(l11,l21);

while(l4!=nullptr){

    cout<<"l4: "<<l4->val<<endl;
    l4=l4->next;
    
}

}