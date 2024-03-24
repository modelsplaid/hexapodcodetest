
#include<iostream>
#include<unordered_map>
#include<vector>

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

class Solution_preord {

public:
    unordered_map<int,int> index;

    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {

        for(vector<int>::iterator itr=inorder.begin();itr<inorder.end();itr++){
            int i=itr-inorder.begin();
            index[*itr]=i;
        }

        return bt(preorder,inorder,0,preorder.size()-1,0,inorder.size()-1);



    }

    TreeNode* bt(vector<int>& preorder, vector<int>& inorder,
                    int pre_lft,int pre_rht,int in_lft,int in_rht) {
        

        if(pre_lft > pre_rht){
            return nullptr;
        }

        int root_val=preorder[pre_lft];
        //cout<<"val: "<<root_val<<endl;
        string str;
        //cin>>str;
        TreeNode *root = new TreeNode(root_val);
        int inord_root_idx = index[root_val];

        int inord_sub_len = inord_root_idx-in_lft;


        root->left = bt(preorder,inorder,pre_lft+1,pre_lft+inord_sub_len,in_lft,inord_root_idx-1);
        root->right = bt(preorder,inorder,pre_lft+inord_sub_len+1,pre_rht,inord_root_idx+1,in_rht);

        return root;
    }


    void test_idx(vector<int> &preorder,vector<int> &inorder){
        for(vector<int>::iterator itr=inorder.begin();itr<inorder.end();itr++){
            int i=itr-inorder.begin();
            index[*itr]=i;
        }

        for(vector<int>::iterator itr=preorder.begin();itr<preorder.end();itr++){
            int id=index[*itr];
            cout<<"val in pre-order: "<<*itr<<" index in in-order: "<<id<<endl;
        }


    }
};

void test_prein_tra(){
    TreeNode *root= new TreeNode(10);TreeNode *lft = new TreeNode(20);
    TreeNode *rht = new TreeNode(30);TreeNode *lft_lft = new TreeNode(40);
    TreeNode *lft_rht = new TreeNode(50);TreeNode *rht_lft = new TreeNode(60);

    root->left = lft;root->right = rht;
    rht->left=rht_lft;lft->left=lft_lft;lft->right=lft_rht;

    //print_bt(root);
    vector<int> preorder={10,20,40,50,30,60};
    vector<int> inorder={40,20,50,10,60,30};
    Solution_preord spd;
    //spd.test_idx(preorder,inorder);
    print_bt(spd.buildTree(preorder,inorder));

}

int main(){
    test_prein_tra();

}


// class Solution {
// private:
//     unordered_map<int, int> index;

// public:
//     TreeNode* myBuildTree(const vector<int>& preorder, const vector<int>& inorder, int preorder_left, int preorder_right, int inorder_left, int inorder_right) {
//         if (preorder_left > preorder_right) {
//             return nullptr;
//         }
        
//         // 前序遍历中的第一个节点就是根节点
//         int preorder_root = preorder_left;
//         // 在中序遍历中定位根节点
//         int inorder_root = index[preorder[preorder_root]];
        
//         // 先把根节点建立出来
//         TreeNode* root = new TreeNode(preorder[preorder_root]);
//         // 得到左子树中的节点数目
//         int size_left_subtree = inorder_root - inorder_left;
//         // 递归地构造左子树，并连接到根节点
//         // 先序遍历中「从 左边界+1 开始的 size_left_subtree」个元素就对应了中序遍历中「从 左边界 开始到 根节点定位-1」的元素
//         root->left = myBuildTree(preorder, inorder, preorder_left + 1, preorder_left + size_left_subtree, inorder_left, inorder_root - 1);
//         // 递归地构造右子树，并连接到根节点
//         // 先序遍历中「从 左边界+1+左子树节点数目 开始到 右边界」的元素就对应了中序遍历中「从 根节点定位+1 到 右边界」的元素
//         root->right = myBuildTree(preorder, inorder, preorder_left + size_left_subtree + 1, preorder_right, inorder_root + 1, inorder_right);
//         return root;
//     }

//     TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
//         int n = preorder.size();
//         // 构造哈希映射，帮助我们快速定位根节点
//         for (int i = 0; i < n; ++i) {
//             index[inorder[i]] = i;
//         }
//         return myBuildTree(preorder, inorder, 0, n - 1, 0, n - 1);
//     }
// };

