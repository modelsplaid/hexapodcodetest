//https://leetcode.cn/problems/climbing-stairs/solutions/286022/pa-lou-ti-by-leetcode-solution/?envType=study-plan-v2&envId=top-100-liked
#include<iostream>
using namespace std;

class Solution {
public:
    int climbStairs(int n) {
        int p = 0, q = 0, r = 1;
        for (int i = 1; i <= n; ++i) {
            p = q; 
            q = r; 
            r = p + q;
        }
        return r;
    }
};

int main()
{
   Solution so;
   int a = so.climbStairs(1);

   std::cout<<"stages: "<<a<<endl;

}