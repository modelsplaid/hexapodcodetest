#include<iostream>
#include<string>

using namespace std;

template<typename T, typename S> 
T tswap(T &a, S &b) {
    T tmp(a); 
    a = b;
    b = tmp;

    return tmp;
}

template<typename T, typename S> 
void t2swap(T a, S b) {
    cout<<"Ta: "<<a<<endl;
    cout<<"Sb: "<<b<<endl;

    cout<<"is_same(a,int): "<<is_same<T,int>:: value<<endl;
    cout<<"is_same(b,int): "<<is_same<S,int>:: value<<endl;
    cout<<"is_same(b,float): "<<is_same<S,float>:: value<<endl;

}

void test1(){
    int a = 2; int b = 3;
    std::cout << "a=" << a << ", b=" << b << std::endl;
    tswap(a, b); // 使用函数模板
    std::cout << "a=" << a << ", b=" << b << std::endl;
    double c = 1.1;
    double d = 2.2; 
    std::cout<<"swap(): "<<tswap(c, d)<<endl;
    std::cout << "c=" << c << ", d=" << d << std::endl;

    string e = "hello";
    float f = 2; 
    t2swap<string,float>(e, f);
}

template <class T, class U> class A {
	T x;
	U y;

public:
	A() { cout << "Constructor Called" << endl; }
};

int test2()
{
	A<char, char> a;
	A<int, double> b;
	return 0;
}

int main(int argc, char* argv[])
{
//test2();
test1();
return 0;
}