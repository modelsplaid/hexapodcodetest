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
