#include<iostream>
#include<math.h>
using namespace std;

struct ListNode{
    int val;
    ListNode* next;
    ListNode(int val):val(val){}
    ListNode(int val,ListNode* next):next(next){}
};



class Node {
public:
    int val;
    Node* next;
    Node* random;
    
    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};

void print_lln(Node *head){

    if(head==nullptr){return;}
    while(head!=nullptr){
        if(head->random != nullptr){
            cout<<"nval: "<<head->val<<"  rand val: "<<head->random->val<< endl;
        }else{
            cout<<"nval: "<<head->val<< endl; 
        }
        head=head->next;
    }
}
void print_ll(ListNode *head){

    if(head==nullptr){
        return;
    }
    while(head!=nullptr){
        cout<<"val: "<<head->val<<endl;
        head=head->next;
    }
}

class Solution_cycle {
public:
    bool hasCycle(ListNode *head) {
        ListNode *fast_ptr=head->next;
        ListNode *slow_ptr=head;

        while(slow_ptr!=nullptr && fast_ptr!=nullptr && fast_ptr->next!=nullptr){
            if(slow_ptr==fast_ptr){
                return true;
            }
            slow_ptr=slow_ptr->next;
            fast_ptr=fast_ptr->next->next;

        }
        return false;
        
    }
};

void test_cycle(){
    ListNode *head = new ListNode(3);
    ListNode *n1 = new ListNode(2);
    ListNode *n2 = new ListNode(0);
    ListNode *n3 = new ListNode(4);
    head->next=n1;
    n1->next=n2;
    n2->next=n3;
    n3->next=n1;
    Solution_cycle sc;
    cout<<"has cycle: "<<sc.hasCycle(head)<<endl;
    // todo next: verify on page
}

class Solution_addnum {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        int len1=0,len2=0;
        ListNode *h1=l1,*h2=l2;
        ListNode *pre_h1,*pre_h2;
        while(h1 != nullptr){
            pre_h1=h1;
            h1=h1->next;
            len1++;
            cout<<"len1: "<<len1<<endl;

        }

        while(h2 != nullptr){
            pre_h2=h2;
            h2=h2->next;
            len2++;
            cout<<"len2: "<<len2<<endl;

        }
        int len=0;
        for(int i=0;i<abs(len1-len2);i++){
            if(len1>len2){
                len=len1;
                pre_h2->next= new ListNode(0);
                pre_h2=pre_h2->next;
            }else{
                len=len2;
                pre_h1->next= new ListNode(0);
                pre_h1=pre_h1->next;
            }
        }

        h1=l1;
        h2=l2;
        ListNode *hr= new ListNode(0);
        ListNode *hreturn=hr;
        int inc = 0;
        while(l1!=nullptr){
            int sval=l1->val+l2->val+inc;
            inc=sval/10;
            hr->next= new ListNode(sval%10);
            hr=hr->next;

            l1=l1->next;
            l2=l2->next;

        }
        if(inc>0){
            hr->next= new ListNode(inc);
        }

    return hreturn->next;
    }
};

void test_add(){
    ListNode *head = new ListNode(1);
    ListNode *n1 = new ListNode(2);
    ListNode *n2 = new ListNode(3);
    ListNode *n3 = new ListNode(4);
    head->next=n1;n1->next=n2;n2->next=n3;

    ListNode *head2 = new ListNode(1);
    ListNode *n12 = new ListNode(8);
    ListNode *n22 = new ListNode(3);
    //ListNode *n32 = new ListNode(9);
    head2->next=n12;n12->next=n22;//n22->next=n32;

    Solution_addnum addn;
    ListNode *reth=addn.addTwoNumbers(head,head2);
    print_ll(reth);
}


class Solution_cpy {
public:
    Node* copyRandomList(Node* head) {
        if(head==nullptr){
            return head;
        }
        if(head->next==nullptr){
            return head;
        }

        // duplicate node
        Node* cur=head;
        while(cur!=nullptr){
            // insert a node
            Node* node = new Node(cur->val);
            node->next=cur->next;
            cur->next=node;

            cur=cur->next->next;
        }

        // assign random ptr
        cur=head;

        while(cur!=nullptr){
            // replace rand ptr
            if(cur->random != nullptr){
                cur->next->random = cur->random->next;
            }
            cur=cur->next->next;
        }

        // split list 
        cur=head;
        Node* noder = head->next;
        Node* node = head->next;
        
        while(cur!=nullptr && cur->next!=nullptr ){
            // original 
            cur->next=cur->next->next;
            cur=cur->next;

            // new lst
            if(node!=nullptr&&node->next!=nullptr){
                node->next=node->next->next;
                node=node->next;
            }


        }
        return noder;
    }
};


void test_cpy_rand(){
    Node *head = new Node(7);
    Node *n1   = new Node(13);
    Node *n2   = new Node(11);
    Node *n3   = new Node(10);
    Node *n4   = new Node(1);
    head->next=n1;n1->next=n2;n2->next=n3;n3->next=n4;
    n1->random=head;
    n4->random=head;
    head->next=n1;n1->next=n2;n2->next=n3;
    n3->random=n2;
    n2->random=n4;
    Solution_cpy scpy;


   Node *head_dup =scpy.copyRandomList(head);
    print_lln(head);
    print_lln(head_dup);
}

int main(){
    //test_cycle();
    //test_add();
    test_cpy_rand();

}