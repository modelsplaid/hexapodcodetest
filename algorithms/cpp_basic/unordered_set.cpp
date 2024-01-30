//https://en.cppreference.com/w/cpp/container/unordered_set

#include <iostream>
#include <unordered_set>
 
void print(const auto& set)
{
    for (const auto& elem : set)
        std::cout << elem << ' ';
    std::cout << '\n';
}
 
int main()
{
    std::unordered_set<int> mySet{2, 7, 1, 8, 2, 8}; // creates a set of ints
    print(mySet);
 
    mySet.insert(5); // puts an element 5 in the set
    mySet.insert(5);
    print(mySet);
 
    if (auto iter = mySet.find(5); iter != mySet.end())
        mySet.erase(iter); // removes an element pointed to by iter
    print(mySet);

    mySet.erase(7); // removes an element 7
    mySet.erase(7);
    print(mySet);
}