//https://www.internalpointers.com/post/writing-custom-iterators-modern-cpp

#include <iterator>
#include <cstddef>
#include <iostream>
using namespace std;
class Integers
{
public:
    struct Iterator 
    {
        using iterator_category = std::forward_iterator_tag;
        using difference_type   = std::ptrdiff_t;
        using value_type        = int;
        using pointer           = int*;
        using reference         = int&;

        Iterator(pointer ptr) : m_ptr(ptr) {}

        reference operator*() const { return *m_ptr; }
        pointer operator->() { return m_ptr; }
        Iterator& operator++() { m_ptr++; return *this; }  
        Iterator operator++(int) { Iterator tmp = *this; ++(*this); return tmp; }
        friend bool operator== (const Iterator& a, const Iterator& b) { return a.m_ptr == b.m_ptr; };
        friend bool operator!= (const Iterator& a, const Iterator& b) { return a.m_ptr != b.m_ptr; };  
    private:
        pointer m_ptr;
    };

    Iterator begin() { return Iterator(&m_data[0]); }
    Iterator end()   { return Iterator(&m_data[200]); }

private:
    int m_data[200];
};

int main(){
    Integers ints;
    for(Integers::Iterator iter=ints.begin();iter==ints.end();iter++){
        *iter=3;


    }

    for(Integers::Iterator iter=ints.begin();iter==ints.end();iter++){
        cout<<"iter: "<<*iter<<endl;
        

    }

    return 0;
}