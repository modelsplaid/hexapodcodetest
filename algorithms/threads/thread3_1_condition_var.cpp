//ref https://en.cppreference.com/w/cpp/thread/condition_variable/wait

#include <chrono>
#include <condition_variable>
#include <iostream>
#include <thread>
 
std::condition_variable cv;
std::mutex cv_m; // This mutex is used for three purposes:
                 // 1) to synchronize accesses to i
                 // 2) to synchronize accesses to std::cerr
                 // 3) for the condition variable cv
int i = 0;
 
// void waits()
// {
//     std::unique_lock<std::mutex> lk(cv_m);
//     std::cerr << "Waiting... \n";
//     cv.wait(lk, []{ return i == 1; });
//     std::cerr << "...finished waiting. i == 1\n";
// }

void waits()
{
    std::unique_lock<std::mutex> lk(cv_m);
    std::cerr << "Waiting... \n";

    auto f=[=](){return i==1;};
    cv.wait(lk,f);
    std::cerr << "...finished waiting i= "<<i<<"\n";
}
 
void signals()
{
    std::this_thread::sleep_for(std::chrono::seconds(1));
    {
        std::lock_guard<std::mutex> lk(cv_m);
        std::cerr << "Notifying...\n";
    }
    i=1;
    cv.notify_all();
}
 
int main()
{
    std::thread t1(waits),t4(signals);
    t1.join();
    t4.join();
}