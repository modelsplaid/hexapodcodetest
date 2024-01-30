#include<thread>
#include<iostream>
#include<deque>

using namespace std;

deque<int> deq;

// A function to be executed by a thread

void consumerFunction(int id)
{
    // Do some work here...
    std::cout << "Thread " << id << " finished" << std::endl;
}

void producerFunction(int id)
{
    // Do some work here...
    std::cout << "Thread " << id << " finished" << std::endl;
}

int main()
{
    // Create two threads
    std::thread c1(consumerFunction, 1);
    std::thread c2(consumerFunction, 2);
    std::thread c3(consumerFunction, 1);
    std::thread c4(consumerFunction, 2);
    std::thread c5(consumerFunction, 1);

    std::thread p1(producerFunction, 1);
    std::thread p2(producerFunction, 2);
    std::thread p3(producerFunction, 1);
    std::thread p4(producerFunction, 2);
    std::thread p5(producerFunction, 1);

    // Wait for the threads to finish

    c1.join();
    c2.join();
    c3.join();
    c4.join();
    c5.join();

    p1.join();
    p2.join();
    p3.join();
    p4.join();
    p5.join();
    
    std::cout << "All threads finished" << std::endl;

    return 0;
}


