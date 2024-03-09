//https://baptiste-wicht.com/posts/2012/04/c11-concurrency-tutorial-advanced-locking-and-condition-variables.html
// C++ program to demonstrate
// multithreading using three
// different callables.

#include<thread>
#include<iostream>

using namespace std;
struct BoundedBuffer {
    int* buffer;
    int capacity;

    int front;
    int rear;
    int count;

    std::mutex lock;

    std::condition_variable not_full;
    std::condition_variable not_empty;

    BoundedBuffer(int capacity) : capacity(capacity), front(0), rear(0), count(0) {
        buffer = new int[capacity];
    }

    ~BoundedBuffer(){
        delete[] buffer;
    }

    void deposit(int data){
        std::unique_lock<std::mutex> l(lock);

        not_full.wait(l, [this](){return count != capacity; });

        buffer[rear] = data;
        rear = (rear + 1) % capacity;
        ++count;

        l.unlock();
        not_empty.notify_one();
    }

    int fetch(){
        std::unique_lock<std::mutex> l(lock);

        auto f=[this](){return count != 0;};

        not_empty.wait(l, f);

        int result = buffer[front];
        front = (front + 1) % capacity;
        --count;

        l.unlock();
        not_full.notify_one();

        return result;
    }
};

void consumer(int id, BoundedBuffer& buffer){
    for(int i = 0; i < 50; ++i){
        int value = buffer.fetch();
        std::cout << "Consumer " << id << " fetched " << value << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
}

void producer(int id, BoundedBuffer& buffer){
    for(int i = 0; i < 75; ++i){
        buffer.deposit(i);
        std::cout << "Produced " << id << " produced " << i << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

int main(){
    BoundedBuffer buffer(200);

    std::thread c1(consumer, 0, std::ref(buffer));
    std::thread p1(producer, 0, std::ref(buffer));

    // std::thread c2(consumer, 1, std::ref(buffer));
    // std::thread c3(consumer, 2, std::ref(buffer));
    // std::thread p2(producer, 1, std::ref(buffer));

    c1.join();
    p1.join();

    // c2.join();
    // c3.join();
    // p1.join();
    // p2.join();

    return 0;
}
