#include<vector>
#include<iostream>
using namespace std;

class Solution {
public:
    int search(vector<int>& nums, int target) {
      
        int left=0;
        int right=nums.size()-1;
        int mid = (nums.size()-1)/2;
        if(nums[0]>target){
            cout<<"too small"<<endl;
            return -1;
        }

        if(nums[right]<target){
            cout<<"too large"<<endl;
            return -1;
        }
        while(left!=right){
            cout<<"--- left: "<<left<<"mid: "<<mid<<" right:"<<right<<endl;
            if(nums[mid]==target){
                return mid;
            }

            if(target<nums[mid]){
                right=mid-1;
                mid=(left+right)/2;
            }

            if(target>nums[mid]){
                left=mid+1;
                mid=(left+right)/2;
            }

        }
        cout<<"not found"<<endl;
        return -1;
    }
};

int main(){
    Solution sol;

    //vector<int> nums={-1,0,3,5,9,12};
    vector<int> nums={1,2,4};
    sol.search(nums,3);
    sol.search(nums,-1);
    sol.search(nums,5);
    //cout<<"idx: "<<sol.search(nums,3)<<endl;
    //cout<<"idx: "<<sol.search(nums,13)<<endl;
    return 0;
}