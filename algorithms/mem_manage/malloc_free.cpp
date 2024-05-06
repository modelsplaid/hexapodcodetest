// C++ program to demonstrate working of malloc()

// cstdlib is used to use malloc function
#include <iostream>
#include <cstdlib>

using namespace std;

void exp(){
	// size_t is an integer data type which can assign
	// greater than or equal to 0 integer values
	size_t s = 0; // s is SIZE

	// malloc declaration/initialization
	int* ptr = (int*)malloc(s);

	// return condition if the memory block is not
	// initialized
	if (ptr == NULL) {
		cout << "Null pointer has been returned";
	}

	// condition printing the message if the memory is
	// initialized
	else {
		cout << "Memory has been allocated at address "
			<< ptr << endl;
	}

	free(ptr);

}

void * malloc_mem(int sz,int block){

    int *ptr,*ptr1;
    int *pt3= new(int);

    ptr1=(int*)calloc(10,sizeof(int));
    ptr=(int*)malloc(sz*block);
    return ptr;
}

void leak(){
    int*ptr=new int;
}

void test1(){
    int* ptr=(int*)malloc_mem(3,5);
    *ptr=12345;
    *(ptr+1)=56789;
    cout<<"*ptr: "<<*ptr<<"ptr+1: "<<(*(ptr+1))<<endl;
    cout<<"size_of(int): "<<sizeof(int)<<endl;
    leak();
    cout<<"max: "<<max(3,4)<<endl;
    cout<<"min: "<<min(3,4)<<endl;

}

int main()
{	
	// create an array with 3 element, type int
	int *ptr = (int*)malloc(3*sizeof(int));
	*ptr=0;
	*(ptr+1)=2;
	*(ptr+2)=4;
	cout<<"ptr arr: "<<*ptr<<" , "<<*(ptr+1)<<", "<<*(ptr+2)<<endl;
	free(ptr);

	return 0;
}
