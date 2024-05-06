//https://leetcode.cn/problems/merge-sorted-array/solutions/666608/he-bing-liang-ge-you-xu-shu-zu-by-leetco-rrb0/?envType=study-plan-v2&envId=top-interview-150
#include<iostream>
#include <vector>
using namespace std;
class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        for (int i = 0; i != n; ++i) {
            nums1[m + i] = nums2[i];
        }
        std::sort(nums1.begin(), nums1.end());
    }
};


int main()
{

vector<int> vec={3,5,2};

auto f=[=](int x,int y){return x>y;};
sort(vec.begin(),vec.end(),f);
for(auto one:vec){
    cout<<"one: "<<one<<endl;
}
}