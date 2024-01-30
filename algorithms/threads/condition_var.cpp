//https://baptiste-wicht.com/posts/2012/04/c11-concurrency-tutorial-advanced-locking-and-condition-variables.html
// C++ program to demonstrate
// multithreading using three
// different callables.
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

        not_empty.wait(l, [this](){return count != 0; });

        int result = buffer[front];
        front = (front + 1) % capacity;
        --count;

        l.unlock();
        not_full.notify_one();

        return result;
    }
};
