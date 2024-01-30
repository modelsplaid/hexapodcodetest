//https://leetcode.cn/problems/symmetric-tree/?envType=study-plan-v2&envId=top-interview-150
//给你一个二叉树的根节点 root ， 检查它是否轴对称。

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool check(TreeNode *p, TreeNode *q) {
        if (p==nullptr && q==nullptr){
            return true;
        }
        if(p==nullptr || q==nullptr){
            return false;
        }

        bool val_cmp = (p->val == q->val);
        bool ptr_cmp = check(p->left,q->right);
        bool ptr_cmp2 = check(p->right,q->left);
        return val_cmp && ptr_cmp && ptr_cmp2;
    }

    bool isSymmetric(TreeNode* root) {
        return check(root, root);
    }
};
