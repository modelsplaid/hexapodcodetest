
class Node {
public:
    int val;
    Node* next;
    Node* random;
    
    Node(int _val) {
        val = _val;
        next = nullptr;
        random = nullptr;
    }
};


class Solution {
public:
    Node* copyRandomList(Node* head) {
        // copy lst
        Node* nhead=head;
        if(head == nullptr){
            return head;
        }

        while(nhead != nullptr){
            Node* newnode = new Node(nhead->val);

            Node* tmp=nhead->next;

            nhead->next = newnode;
            newnode->next=tmp;
            nhead= tmp;    

        }

        // assign rand
        nhead=head;

        while(nhead != nullptr){
            if(nhead->random != nullptr){
                nhead->next->random=nhead->random->next;

            }
            nhead = nhead->next->next;

        }

        // // split 
        nhead=head;
        Node *newhead = nhead->next;
        Node *rnewhead=newhead;
        while(newhead->next != nullptr){
            
            if(nhead->next->next !=nullptr){
                nhead->next = nhead->next->next;
            }

            newhead->next=newhead->next->next;
        }
        return rnewhead;
    }
};
