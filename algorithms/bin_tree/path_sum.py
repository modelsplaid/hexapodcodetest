#https://leetcode.cn/problems/path-sum/solutions/318487/lu-jing-zong-he-by-leetcode-solution/?envType=study-plan-v2&envId=top-interview-150
class Solution {
public:
    bool hasPathSum(TreeNode* root, int targetSum) {
        if(root==nullptr){
            return false;
        }
        if(root->val==targetSum){
            return true;
        }
        if(hasPathSum(root->left,targetSum-root->val)||hasPathSum(root->right,targetSum-root->val)){
            return true;
        }else{
            return false;
        }

    }
};
