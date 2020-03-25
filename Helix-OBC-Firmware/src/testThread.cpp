#include "testThread.h"
#include <thread>
#include <chrono>
#include <boost/log/trivial.hpp>

void testing(bounded_buffer<struct can_frame>& thing) {
    struct can_frame data;
    data.can_id = CANIDS_HELIUM_PRESSURE_PT_DATA;
    data.data[0] = 'h';
    data.data[1] = 'e';
    data.data[2] = 'l';
    data.data[3] = 'l';
    data.data[4] = 'o';
    data.data[5] = '\0';
    thing.push_front(data);

    std::this_thread::sleep_for(std::chrono::milliseconds(10000));
    data.can_id = CANIDS_QUIT;
    thing.push_front(data);
    BOOST_LOG_TRIVIAL(warning) << "End of testing thread";
}

