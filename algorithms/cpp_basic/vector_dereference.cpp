#include<vector>
#include<iostream>
using namespace std;
int main() {
    // Create a vector
    std::vector<int> myVector;

    myVector.push_back(3);
    myVector.push_back(6);
    myVector.clear();
    myVector.push_back(9);
    myVector.push_back(90);
    myVector.resize(0);
    // Create a pointer to the vector
    std::vector<int>* ptrVector = new vector<int>;

    if(myVector.begin()==myVector.end()){
            cout<<"Empty vector"<<endl;
        }

    for(std::vector<int>::iterator it=myVector.begin();it<=myVector.end();it++){
        cout<<"iter: "<<*it<<endl;

    }
    // Access elements using the vector pointer
    
    //myVector.clear();

    if(myVector.size()!=0){
        std::cout << "First element: " << myVector[0] << std::endl;
        std::cout << "Second element: " << (*ptrVector)[1] << std::endl;
    }
    return 0;
}
