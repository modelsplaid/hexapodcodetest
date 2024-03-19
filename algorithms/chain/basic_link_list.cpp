#include<iostream>
using namespace std;

struct ListNode{

    int value=0;
    ListNode* next={nullptr} ;
    ListNode(int x){value=x; next=nullptr;};
    ListNode(int x,ListNode *node){value=x;next=node;};

};

ListNode * insert_front(ListNode * &head){

    ListNode * ptr = new ListNode(6);
    ptr->value=6;
    ptr->next=head;
    head=ptr;

    return head;

}

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
        cout<<"value: "<<head->value<<endl;
        head=head->next;
    }
}


ListNode* delete_end(ListNode *head){

    ListNode *fst=head;
    if(head==nullptr){
        cout<<"empty ll"<<endl;
        return nullptr;
    }

    if(head->next == nullptr){
        free(head);
        cout<<"one ll"<<endl;
        return nullptr;
    }

    ListNode *pre;
    while(head->next!=nullptr){
        pre=head;
        head=head->next;
    }
    pre->next=nullptr;
    //free(head);
    delete(head);

    return fst;

}

void test_insert(){
    ListNode * head= new ListNode(3);
    ListNode * nhead=insert_front(head);
    insert_end(head);
    print_ll(head);
}

void test_delete(){
    ListNode * head= new ListNode(3);
    insert_end(head);
    insert_end(head);
    insert_end(head);
    print_ll(head);

    cout<<"del end"<<endl;
    delete_end(head);
    delete_end(head);
    print_ll(head);

}


ListNode* swap_lst(ListNode *head){
    ListNode *head2=head->next;
    head->next=nullptr;
    head2->next=head;

    ListNode *head3=head2->next;
    head->next=nullptr;
    head2->next=head;

    return head2;
}

void test_swap(){
    ListNode * head = insert_end(nullptr,3);
    insert_end(head,6);
    insert_end(head,9);
    print_ll(head);

    head=swap_lst(head);
    print_ll(head);
}

ListNode* find_middle(ListNode *head){
    ListNode *slwp;
    ListNode *fstp;
    ListNode *mid_l;
    // slwp=head->next;
    // fstp=head->next->next;

    slwp=head;
    fstp=head;

    while((fstp!= nullptr) && (fstp->next != nullptr) ){
        mid_l=slwp;
        slwp=slwp->next;
        fstp=fstp->next->next; // tood: here
    }

    if(fstp == nullptr){
        cout<<"even fs"<<endl;
        return mid_l;

    }else if(fstp->next == nullptr){
            cout<<"fs->next"<<endl;
        }
    
    return slwp;
}

void test_find_middle(){
    ListNode * head = insert_end(nullptr,3);
    insert_end(head,6);
    insert_end(head,9);
    insert_end(head,12);
    //insert_end(head,15);
    auto mid =find_middle(head);
    print_ll(mid);
}

ListNode * reverse_ll(ListNode * head){

    ListNode *p=nullptr,*c=nullptr,*n=nullptr;
    c=head;
    //while(c!=nullptr && c->next != nullptr){
    while(c!=nullptr){
        n=c->next;
        c->next=p;
        p=c;
        c=n;
    }

    return p;

}

void test_reverse_ll(){
    ListNode * head = insert_end(nullptr,3);
    insert_end(head,6);
    insert_end(head,9);
    insert_end(head,12);
    insert_end(head,15);
    auto rh = reverse_ll(head);
    print_ll(rh);
}


void del_ith_node(ListNode *head){
    int ith = 3;
    int len = 0;

    ListNode *tmp=head;

    while(tmp != nullptr){
        len = len+1;
        tmp = tmp->next;
    }
    cout<<"len: "<<len<<endl;

    for(auto i=0;i<len-ith;i++){
        head=head->next;
    }

    ListNode *choose_nod = head;
    cout<<"choose val: "<<choose_nod->value<<endl;
    //replace node
    choose_nod->value = choose_nod->next->value;
    choose_nod->next  = choose_nod->next->next;
    //delete choose_nod->next;

}

void test_delete_node(){
    ListNode * head = insert_end(nullptr,3);
    insert_end(head,6);
    insert_end(head,9);
    insert_end(head,12);
    insert_end(head,15);
    del_ith_node(head);
    print_ll(head);

}


ListNode* del_rep(ListNode *head){

    ListNode *dumy= new ListNode(0,head);

    ListNode *cur= dumy;
    while(cur->next && cur->next->next ){

        if(cur->next->value == cur->next->next->value){
            int x = cur->next->value;
            while((cur->next!=nullptr) && (x==cur->next->value)){
                cur->next=cur->next->next;
            }

        }else{
            cur=cur->next;
        }
    }
    return dumy->next;
}

void test_delete_repetitive(){
    ListNode * head = insert_end(nullptr,3);
    insert_end(head,6);
    insert_end(head,9);
    insert_end(head,8);
    insert_end(head,8);
    auto nh=del_rep(head);
    print_ll(nh);
}

ListNode* rot_ll(ListNode* head,int k=2){
    ListNode* fst=head;
    ListNode* cur=head;
    ListNode* sec=fst->next;
    while(cur->next!=nullptr ){
        cur=cur->next;
    }

    cur->next=head; // connect tail
    sec=fst->next;
    //for(auto i=0;i<k-1;i++){
    for(auto i=0;i<k;i++){
        fst=fst->next;
        sec=fst->next;
    }
    fst->next=nullptr;
    return sec;
}

void test_rot_ll(){
    ListNode * head = insert_end(nullptr,4);
    insert_end(head,6);
    insert_end(head,9);
    auto fst=rot_ll(head);
    print_ll(fst);
}


ListNode *sepa_ll(ListNode *head,int val){
    ListNode *small=new ListNode(0,head);
    ListNode *fst=small;

    ListNode *large=new ListNode(0,head);
    ListNode *sec=large;

    ListNode *cur=new ListNode(0,head);

    if(head==nullptr){
        return nullptr;
    }

    if(head->next==nullptr){
        return cur;
    }

    while(cur->next!=nullptr){
        
        if(cur->next->value<val){
            small->next=cur->next;
            small=small->next;

        }else{
            
            large->next=cur->next;
            large=large->next;
            //cout<<"large v: "<<large->value<<endl;
        }
        cur=cur->next;
    }
    small->next=sec->next;

    return fst->next;
}

void test_sepa_ll(){
    ListNode * head = insert_end(nullptr,4);
    insert_end(head,5);
    insert_end(head,6);
    insert_end(head,9);
    auto sep=sepa_ll(head,6);
    print_ll(sep);
}


class Solution_hasCycle {
    // verified
public:
    bool hasCycle(ListNode *head) {

    if(head == nullptr){
        return false;
    }

    if(head->next == nullptr){
        return false;
    }

    if(head==head->next){
        return true;
    }

    ListNode *slp=head;
    ListNode *fsp=head->next->next;

    while(fsp!=nullptr && fsp->next!=nullptr){

        if(slp == fsp){
            return true;
        }
        fsp=fsp->next->next;
        slp=slp->next;
    }
    return false;
    }
};

void test_cycle(){
    ListNode * head = insert_end(nullptr,4);
    // insert_end(head,5);
    // insert_end(head,6);
    // insert_end(head,9);

    Solution_hasCycle sol;
    cout<<"has cycle: "<<sol.hasCycle(head)<<endl;

}


class Solution_addNum {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {

        int len1=0,len2=0,len=0;
        ListNode *cur1=l1,*cur2=l2;
        ListNode *result=new ListNode(0);
        ListNode *pre1=nullptr,*pre2=nullptr,*rh=result;

        while(cur1!=nullptr){
            pre1=cur1;
            cur1=cur1->next;
            len1++;
        }

        while(cur2!=nullptr){
            pre2=cur2;
            cur2=cur2->next;
            len2++;
        }
        len=len1;

        if(len1>len2){
            len=len1;
            for(auto i=0;i<len1-len2;i++){
                pre2->next = new ListNode(0);
                pre2 = pre2->next;
            }
        }

        if(len1<len2){
            len=len2;
            for(auto i=0;i<len2-len1;i++){
                pre1->next = new ListNode(0);
                pre1 = pre1->next;
            }
        }

        int incre=0;
        for(auto i=0;i<len;i++){
            
           int val = (l1->value + l2->value+incre)%10;
           incre = (l1->value + l2->value+incre)/10;

           result->next = new ListNode(val);
           result=result->next;
           l1=l1->next;
           l2=l2->next;
        }

        if(incre>0){
            result->next = new ListNode(incre);

        }

        return rh->next;

    }
};


void test_addNum(){
    ListNode * head = insert_end(nullptr,2);
    insert_end(head,4);
    //insert_end(head,3);

    ListNode * head2 = insert_end(nullptr,5);
    insert_end(head2,6);
    insert_end(head2,4);

    Solution_addNum san;
    ListNode * result=san.addTwoNumbers(head,head2);
    print_ll(result);

}

class Solution_mergell {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode *l1=list1,*l2=list2;
        ListNode *hd= new ListNode(0);
        ListNode *rhd= hd;


        if(list1==nullptr || list2==nullptr){
            if(list1!=nullptr){
                return list1;
            }
            if(list2!=nullptr){
                return list2;
            }

        }

        while((l1!=nullptr) && (l2!=nullptr)){
            if(l1->value > l2->value){
                hd->next = l2;
                hd=hd->next;

                if(l2->next == nullptr){
                    l2->next = l1;
                    break;
                }

                l2=l2->next;
            }else{
                hd->next = l1;
                hd=hd->next;

                if(l1->next == nullptr){
                    l1->next = l2;
                    break;
                }

                l1=l1->next;

            }
        }


        return rhd->next;
    }
};

void test_merge(){
    ListNode * head = insert_end(nullptr,1);
    insert_end(head,2);
    insert_end(head,4);

    ListNode * head2 = insert_end(nullptr,1);
    insert_end(head2,3);
    insert_end(head2,4);

    Solution_mergell smer;
    ListNode * result=smer.mergeTwoLists(head,head2);
    print_ll(result);

}




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

void print_node(Node *head){

    if(head==nullptr){
        return;
    }

    while(head!=nullptr){
        if(head->random != nullptr){
            cout<<"value: "<<head->val<<" next add: "<<head->next<< " rand val: "<<head->random->val<<endl;
        }else{
            cout<<"value: "<<head->val<<" next add: "<<head->next<<endl;
        }
        head=head->next;
    }
}

class Solution_cplst {
public:
    Node* copyRandomList(Node* head) {
    
    //duplicate llst
    for(Node* cur=head;cur!=nullptr;cur=cur->next->next){
        Node* cur_p = new Node(cur->val);
        cur_p->next = cur->next;
        cur->next=cur_p;
    }

    //copy rand ptr
    for(Node* cur=head;cur!=nullptr;cur=cur->next->next){
        if(cur->random!=nullptr){
            cur->next->random=cur->random->next;
        }else{
            cur->next->random=nullptr;
        }
    }



    //break link
    Node* duph=head->next;

    Node* cur=head;
    while(cur!=nullptr){

        Node* nodeNew=cur->next;
        cur->next=cur->next->next;

        if(nodeNew->next != nullptr){
            nodeNew->next= nodeNew->next->next;
        }else{
            nodeNew->next=nullptr;
        }   

        cur=cur->next;

    }
 
    return duph;

    }
};


void test_rand_lst(){
    Node *head = new Node(3);
    Node *two  = new Node(2);
    Node *thr  = new Node(1);

    head->next=two;
    two->next=thr;
    head->random=thr;

    print_node(head);
    Solution_cplst scp;
    Node *duph = scp.copyRandomList(head);

    cout<<"dup: "<<endl;
    print_node(duph);
    cout<<"orogin: : "<<endl;
    print_node(head);
}

class Solution_delri {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        // loop all 
        int num=0;
        if(head == nullptr){
            return head;
        }
        if(head->next == nullptr){
            return nullptr;
        }

        for (ListNode *node=head;node!=nullptr;node=node->next){
            num++;
        }
        int ith=(num-n-1);
        if(ith<0){
            head=head->next;
            return head;
        }

        ListNode* cur=head;
        for(int i=0;i<ith;i++){
            cur=cur->next;
        }
        cur->next=cur->next->next;
        return head;

    }
};

void test_delete_rnode(){
    ListNode * head = insert_end(nullptr,3);
    insert_end(head,6);
    insert_end(head,9);
    insert_end(head,12);
    insert_end(head,15);
    Solution_delri del;
    print_ll(head);
    ListNode* res=del.removeNthFromEnd(head,5);
    print_ll(res);

}

int main(){
    //test_delete();
    //test_swap();
    //test_find_middle();
    //test_reverse_ll();
    //test_delete_node();
    //test_delete_repetitive();
    //test_rot_ll();
    //test_sepa_ll();
    //test_cycle();
    //test_addNum();
    //test_merge();
    //test_rand_lst();
    test_delete_rnode();

    return 0;
}
