#include "testThread.h"
#include <thread>
#include <chrono>
#include <boost/log/trivial.hpp>
#include "eventTimer.h"
#include "CANIDs.h"

void testing(bounded_buffer<struct can_frame>& thing) {
    struct can_frame data;

    BOOST_LOG_TRIVIAL(trace) << "Start test thread";

    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    data.can_id = CANIDS_HELIUM_PRESSURE_PT_DATA;
    struct helium_pressure_pt_data canData;
    canData.helium_pressure = 100;

    for (unsigned int i = 0; i < 50*10; i++) {
        canData.utc_time = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now().time_since_epoch()).count();
#if 0
        if (canData.helium_pressure < 320) {
            canData.helium_pressure += 2;
        }
#elif 0
        if (canData.helium_pressure > 80) {
            canData.helium_pressure -= 1;
        }
#endif
        memcpy(data.data, &canData, sizeof(struct helium_pressure_pt_data));

        thing.push_front(data);
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }

    data.can_id = CANIDS_QUIT;
    thing.push_front(data);
    BOOST_LOG_TRIVIAL(warning) << "End of testing thread";
}

