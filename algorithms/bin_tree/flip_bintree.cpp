// https://leetcode.cn/problems/invert-binary-tree/?envType=study-plan-v2&envId=top-interview-150
// 给你一棵二叉树的根节点 root ，翻转这棵二叉树，并返回其根节点。
#include<iostream>

struct TreeNode{
    TreeNode *left;
    TreeNode *right;
    int val;
    TreeNode(): val(0),left(nullptr),right(nullptr){}
    TreeNode(int val):val(val),left(nullptr),right(nullptr){}
    TreeNode(int val,TreeNode *left,TreeNode *right):val(val),left(left),right(right){}
};

class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (root==nullptr){
            return nullptr;
        }
        
        TreeNode* left  = invertTree(root->left);
        TreeNode* right = invertTree(root->right);
        root->left=right;
        root->right=left;

        return root;
    }
};

int main(){
    TreeNode *tn = new TreeNode(6);
    std::cout<<"val: "<<tn->val<<std::endl;
}