#include <iostream>
#include "event.h"
#include "eventTimer.h"
#include "testThread.h"
#include "CANIDs.h"
#include "bounded_buffer.hpp"
#include <thread>
#include <stdint.h>

int main () {
    bounded_buffer<struct can_frame> CANBus(50);

    std::thread eventThread(eventParse, std::ref(CANBus));

    std::thread testThreadThread(testing, std::ref(CANBus));

    std::thread eventTimerThread(eventTimer, std::ref(CANBus));

    eventThread.join();
    testThreadThread.join();
    eventTimerExit();
    eventTimerThread.join();

    return 0;
}

