#include<iostream>
#include<queue>
#include<stack>

using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

void print_bt(TreeNode *root){

    if(root==nullptr){
        return;
    }
    cout<<"val: "<<root->val<<endl;

    print_bt(root->left);
    print_bt(root->right);
}


TreeNode * insert_bt(){
    TreeNode *lft  = new TreeNode(1);
    TreeNode *rht  = new TreeNode(3);
    TreeNode *root = new TreeNode(2,lft,rht);
    print_bt(root);
    return root;
}

class Solution_mxlen {
public:
    int maxDepth(TreeNode* root) {

        if(root == nullptr){
            return 0;
        } 

        int l=maxDepth(root->left)+1;
        int r=maxDepth(root->right)+1;  
        if(l>r){
            return l;
        }else{
            return r;
        }  
    }
};

void test_max_len(){

    TreeNode *lft      = new TreeNode(1);
    TreeNode *rht      = new TreeNode(3);
    TreeNode *rht_rht  = new TreeNode(4);
    rht->right=rht_rht;

    TreeNode *root = new TreeNode(2,lft,rht);
    Solution_mxlen mlen;
    cout<<"max dep: "<< mlen.maxDepth(root)<<endl;
}


class Solution_samt {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if(p==nullptr && q==nullptr){
            return true;
        }

        if(p==nullptr||q==nullptr ){
            return false;
        }

        if(p->val != q->val){
            return false;
        }

        if(p->val == q->val){
            bool l = isSameTree(p->left,q->left);
            bool r = isSameTree(p->right,q->right);
            if(l==true && r == true){
                return true;
            }else{

                return false;
            }

        }
        return false;


    }
};

void test_samt(){
    Solution_samt st;

    TreeNode *lft      = new TreeNode(1);
    TreeNode *rht      = new TreeNode(3);
    TreeNode *rht_rht  = new TreeNode(4);
    rht->right=rht_rht;
    TreeNode *root = new TreeNode(2,lft,rht);

    TreeNode *lft2      = new TreeNode(1);
    TreeNode *rht2      = new TreeNode(3);
    TreeNode *rht_rht2  = new TreeNode(4);
    rht2->right=rht_rht2;
    TreeNode *root2 = new TreeNode(2,lft2,rht2);

    Solution_samt ssamt;
    cout<<"ssamt: "<<ssamt.isSameTree(root,root2)<<endl;
}


class Solution_ivtt {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(root == nullptr){
            return nullptr;
        }
        if(root->left==nullptr){
            return root->left;
        }

        if(root->right==nullptr){
            return root->right;
        }

        TreeNode* tmp = root->left;
        root->left = root->right;
        root->right = tmp;

        invertTree(root->left);
        invertTree(root->right);

        return root;

    }
};


void test_ivtt(){

    TreeNode *lft      = new TreeNode(1);
    TreeNode *rht      = new TreeNode(3);
    TreeNode *rht_rht  = new TreeNode(4);
    rht->right=rht_rht;
    TreeNode *root = new TreeNode(2,lft,rht);

    print_bt(root);
    
    Solution_ivtt ivt;
    ivt.invertTree(root);
    cout<<"-------"<<endl;
    print_bt(root);
}


class Solution_symt {
public:
    bool isSymmetric(TreeNode* root) {
        if(root->left->val == root->right->val){
            return true;
        }else{
            return false;
        }

        if(root->left == nullptr && root->right==nullptr){
            return true;
        }else if(root->left != nullptr && root->right!=nullptr) {
            bool l = isSymmetric(root->left);
            bool r = isSymmetric(root->right);

            if(l==true && r==true){
                return true;
            }else{
                return false;
            }
        }else{
            return false;
        }



    }
};

void test_symt(){

    TreeNode *lft      = new TreeNode(2);
    TreeNode *rht      = new TreeNode(2);
    TreeNode *rht_rht  = new TreeNode(4);
    //rht->right=rht_rht;
    TreeNode *root = new TreeNode(2,lft,rht);

    print_bt(root);
    
    Solution_symt symt;
    cout<<"symt: "<<symt.isSymmetric(root)<<endl;
}

void test_stack(){
    stack<int> a;
    queue<int> b;
    a.push(3);
    a.push(6);
    a.push(9);
    cout<<"a.top: "<<a.top()<<endl;
    a.pop();

    cout<<"a.top: "<<a.top()<<endl;
    a.pop();

    b.push(1);
    b.push(2);
    b.push(3);
    cout<<"b.front: "<<b.front()<<endl;
    b.pop();
    cout<<"b.pop: "<<b.front()<<endl;
    b.pop();

    
}

int main(){
    //insert_bt();
    //test_max_len();
    //test_samt();
    //test_ivtt();
    //test_symt();
    test_stack();


}
