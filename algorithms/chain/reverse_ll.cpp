#include<iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

ListNode * insert_end(ListNode *head=nullptr,int val=9){
    if(head==nullptr){
        head = new ListNode(val);
        return head;
    }

    ListNode * end = new ListNode(val);
    while(head->next!=nullptr){
        head=head->next;
    }
    head->next=end;

    return head;

}

void print_ll(ListNode *head){
    if(head==nullptr){
        return;
    }

    while(head!=nullptr){
        cout<<"value: "<<head->val<<endl;
        head=head->next;
    }
}


class Solution_revl {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* pre= nullptr;
        ListNode* cur=head;
        ListNode* n=head->next;

        while(cur!=nullptr){
            n=cur->next; // update next 
            cur->next=pre; 
            
            pre=cur;      // update pre
            cur=n;

        }

        return pre;

    }
};


void test_rev1(){
    ListNode * head = insert_end(nullptr,1);
    insert_end(head,2);
    insert_end(head,3);
    insert_end(head,4);
    Solution_revl srevl;
    ListNode *rev= srevl.reverseList(head);
    print_ll(rev);
}

class Solution_revl2 {
public:
    ListNode* reverseList(ListNode* head,int left=2,int right=4) {


        ListNode* pre_lptr= nullptr;
        ListNode* pas_rptr= nullptr;

        ListNode* lptr= nullptr;
        ListNode* rptr= nullptr;

        // find lft rht ptr
        for(ListNode *node=head;node->next !=nullptr;node=node->next){
            if(node->next->val==left){
                pre_lptr=node;
                lptr=node->next;
            }
            if(node->val==right){
                rptr = node;
                pas_rptr=node->next;
            }
            
        }

        pre_lptr->next=rptr;

        // start reverse
        //rptr->next=nullptr;
        rptr->next=lptr;
        ListNode* head_lptr=lptr;

        ListNode* pre_ptr=nullptr;
        ListNode* cur_ptr=head_lptr;
        ListNode* nex_ptr=nullptr;

        while(cur_ptr != nullptr){
            cout<<"lst: "<<cur_ptr->val<<endl;
            nex_ptr=cur_ptr->next;
            cur_ptr->next=pre_ptr;

            pre_ptr=cur_ptr;
            cur_ptr=nex_ptr;
        }

        pre_ptr->next = pas_rptr;

        return head;

    }
};

void test_rev2(){
    ListNode * head = insert_end(nullptr,1);
    insert_end(head,2);
    insert_end(head,3);
    insert_end(head,4);
    insert_end(head,5);
    insert_end(head,6);
    Solution_revl2 srevl2;
    ListNode *rev= srevl2.reverseList(head);
    print_ll(head);
}

int main(){

    test_rev2();
}