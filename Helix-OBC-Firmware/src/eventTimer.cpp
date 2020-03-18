#include "eventTimer.h"
#include <queue>
#include <thread>
#include <chrono>
#include <condition_variable>
#include <mutex>

//!< Contains a can frame to be sent to the CANBUS queue after the wakeTime has passed.
struct timer_can_frame {
    struct can_frame canFrame;
    std::chrono::time_point<std::chrono::system_clock> wakeTime;
    // Custom comparison function for priority queue
    bool operator()(const struct timer_can_frame& lhs, const struct timer_can_frame& rhs) {
        if (lhs.wakeTime == rhs.wakeTime) {
            return lhs.canFrame.can_id < rhs.canFrame.can_id;
        }
        return lhs.wakeTime < rhs.wakeTime;
    }
};

static std::priority_queue<struct timer_can_frame, std::vector<struct timer_can_frame>, timer_can_frame> timerQueue;
static std::mutex timerQueueMutex;
static std::condition_variable timerQueueCV;
std::atomic<bool> runEventTimer;

/**
 * @brief Event timer thread that pushes can_frames onto the the CANBus queue at designated times.
 * @param[in] &CANBus Queue containing all of the messages to be processed by the core event thread.
 * @return
 */
void eventTimer(bounded_buffer<struct can_frame>& CANBus) {
    struct timer_can_frame timerFrame;
    runEventTimer = true;
    while (runEventTimer == true) {
        std::unique_lock<std::mutex> lk(timerQueueMutex);

        // Wait until the timerQueue is not empty
        timerQueueCV.wait(lk, []{return !timerQueue.empty();});

        // Check if the current thread needs to exit
        if (!runEventTimer) {
            break;
        }

        // Get the highest priority frame off the queue
        timerFrame = timerQueue.top();

        // Wait until it's either time to send the message or a new message has been put onto the priority queue
        timerQueueCV.wait_until(lk, timerFrame.wakeTime);

        // Time has ellapsed and the timerQueue has not been cleared, send message
        if (std::chrono::system_clock::now() > timerFrame.wakeTime && !timerQueue.empty()) {
            CANBus.push_front(timerFrame.canFrame);
            timerQueue.pop();
        }
    }
}

uint32_t eventTimerPushEvent(can_frame *frame, int milliseconds) {
    struct timer_can_frame timerFrame;
    timerFrame.canFrame = *frame;
    timerFrame.wakeTime = std::chrono::system_clock::now() + std::chrono::milliseconds(milliseconds);

    std::lock_guard<std::mutex> lk(timerQueueMutex);
    timerQueue.push(timerFrame);
    timerQueueCV.notify_one();
    return 0;
}

uint32_t eventTimerClear() {
    std::lock_guard<std::mutex> lk(timerQueueMutex);
    while (!timerQueue.empty()) {
        timerQueue.pop();
    }
    timerQueueCV.notify_one();
    return 0;
}

uint32_t eventTimerExit() {
    runEventTimer = false;
    struct can_frame timerFrame;
    timerFrame.can_id = 0;
    // Push false event to get eventTimer thread out of waiting for data on queue
    eventTimerPushEvent(&timerFrame, 0);
    return 0;
}
