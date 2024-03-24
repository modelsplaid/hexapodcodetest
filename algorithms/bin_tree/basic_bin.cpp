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


class Solution_ksmall {
public:
    int kthSmallest(TreeNode* root, int k) {

        stack<TreeNode*> stn;
        TreeNode *cur=root;
        while(root != nullptr||stn.empty()==false){
            while(root!=nullptr){
                stn.push(root);
                root=root->left;
            }
            if(stn.empty()==true){
                return 0;
            }

            root=stn.top();
            cout<<"pop val: "<<root->val<<endl;
            stn.pop();
            root=root->right;

        }
        return 0;
    }
};

void test_nsmall(){

    TreeNode *lft      = new TreeNode(1);
    TreeNode *rht      = new TreeNode(4);
    TreeNode *lft_rht  = new TreeNode(2);
    lft->right=lft_rht;
    TreeNode *root = new TreeNode(3,lft,rht);

    Solution_ksmall sks;
    sks.kthSmallest(root,1);
    //print_bt(root);
}


class Solution_pre_tra {

public:

    vector<int> preorderTraversal_rec(TreeNode* root) {
        vector<int> vec;

        preord_rec(root,vec);
        return vec;
    }

    void preord_rec(TreeNode* root,vector<int> &vec){

        if(root==nullptr){
            return;
        }
        vec.push_back(root->val);
        preord_rec(root->left,vec);
        preord_rec(root->right,vec);
    }


vector<int> preorderTraversal_itr(TreeNode* root) {

        stack<TreeNode*> stn;
        TreeNode *cur=root;
        vector<int> vec;
        while(root != nullptr||stn.empty()==false){
            while(root!=nullptr){
                vec.push_back(root->val);

                stn.push(root);
                root=root->left;
            }
            if(stn.empty()==true){
                return vec;
            }

            root=stn.top();
            stn.pop();
            root=root->right;

        }
        return vec;
    }
};


void test_pre_tra(){
    TreeNode *rht      = new TreeNode(2);
    TreeNode *rht_lft  = new TreeNode(3);
    rht->left = rht_lft;
    TreeNode *root = new TreeNode(1,nullptr,rht);
    Solution_pre_tra spt;
    //vector<int>  vec= spt.preorderTraversal_rec(root);
    vector<int>  vec= spt.preorderTraversal_itr(root);
    for(vector<int>::iterator itr=vec.begin();itr!=vec.end();itr++){
        cout<<"vec: val: "<<*itr<<endl;
    }

    //print_bt(root);
}


class Solution_post_odr {
public:
    void pos_odr(TreeNode* root, vector<int>& res) {
        if (!root) {
            return;
        }
        pos_odr(root->left, res);
        pos_odr(root->right, res);
        res.push_back(root->val);

    }
    vector<int> postTraversal(TreeNode* root) {
        vector<int> res;
        pos_odr(root, res);
        return res;
    }
};


void test_post_tra(){
    TreeNode *root= new TreeNode(3);TreeNode *lft = new TreeNode(9);
    TreeNode *rht = new TreeNode(4);TreeNode *rht_lft = new TreeNode(5);
    TreeNode *rht_rht = new TreeNode(7);
    root->left = lft;root->right = rht;rht->left=rht_lft;rht->right=rht_rht;
    Solution_post_odr pdr;

    vector<int> vec;
    vec=pdr.postTraversal(root);
    for(auto itr=vec.begin();itr<vec.end();itr++){
        cout<<" post idx: "<<itr-vec.begin()<<": "<<*itr<<endl;
    }

}


class Solution_mid_odr {
public:
    void inorder(TreeNode* root, vector<int>& res) {
        if (!root) {
            return;
        }
        inorder(root->left, res);
        res.push_back(root->val);
        inorder(root->right, res);
    }
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        inorder(root, res);
        return res;
    }
};

void test_mid_tra(){
    TreeNode *root= new TreeNode(3);TreeNode *lft = new TreeNode(9);
    TreeNode *rht = new TreeNode(4);TreeNode *rht_lft = new TreeNode(5);
    TreeNode *rht_rht = new TreeNode(7);
    root->left = lft;root->right = rht;rht->left=rht_lft;rht->right=rht_rht;
    Solution_mid_odr smo;
    vector<int> vec;
    smo.inorder(root,vec);
    for(auto itr=vec.begin();itr<vec.end();itr++){
        cout<<"idx: "<<itr-vec.begin()<<": "<<*itr<<endl;
    }
}

int main(){
    //insert_bt();
    //test_max_len();
    //test_samt();
    //test_ivtt();
    //test_symt();
    //test_nsmall();
    //test_pre_tra();
    //test_pose_tra();
    //test_mid_tra();
    test_post_tra();
}
