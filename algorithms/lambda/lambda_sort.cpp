#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
//https://leetcode.cn/leetbook/read/cmian-shi-tu-po/vwegz6/
int sort_arr(){

    int arr[4] = {4, 2, 3, 1};
    //对 a 数组中的元素进行升序排序
    //sort(arr, arr + 4, [=](int x, int y){ return x < y; } );

    auto f=[=](int x, int y){ return x > y; };
    sort(arr, arr + 4, f);
    sort(arr, arr + 4,greater<int>());

    for(int n : arr){
        cout << n << " ";
    }
    return 0;

}

int sor_vec(){
    vector<int> avec={4,2,3,1};
    for(auto one:avec){
        cout<<one<<endl;
    }

    //for (auto &one:avec){
    for (auto &one:avec){
        one=1;
    }

    for (auto one:avec){

        cout<<one<<endl;
    }
    return 0;

}

int main()
{
    //sort_arr();
    sor_vec();
}
