#include "groundSafeState.h"
#include "eventTimer.h"
#include <iostream>
#include <boost/log/trivial.hpp>

#include <thread>
#include <chrono>

static enum STATES parseHeliumPressurePTData(can_frame *data) {
    //struct helium_pressure_pt_data *pressurePTData = data;
    //! Print out CANID and Data from the can_frame
    //std::cout << "CANID: " << data->can_id << "\n";
    //std::cout << "Data: " << data->data << "\n";

    struct helium_pressure_pt_data *canData = reinterpret_cast<struct helium_pressure_pt_data *>(data->data);

//    BOOST_LOG_TRIVIAL(trace) << "CANID: " << data->can_id;
//    BOOST_LOG_TRIVIAL(info) << "Data: " << canData->helium_pressure;

    if (canData->helium_pressure > 50) {
        BOOST_LOG_TRIVIAL(warning) << "Warning helium pressure too high: " << canData->helium_pressure;
    }

    //! Continue in the ground safe state state.
    return STATE_GROUND_SAFE;
}

/**
 * @brief Called when entering the ground safe state
 * @return Returns 0.
 * 
 * Prints a warning to stdout that the system is entering the ground safe state.
 */
enum STATES groundSafeStateEnter(can_frame *data) {
    BOOST_LOG_TRIVIAL(info) << "Entering Ground Safe State.";
    BOOST_LOG_TRIVIAL(warning) << "Opening valves.";
    
    return STATE_GROUND_SAFE;
}

/**
 * @brief Called when exiting the ground safe state
 * @return Returns 0.
 * 
 * Prints a warning to stdout that the system is exiting the ground safe state.
 */
enum STATES groundSafeStateExit(can_frame *data) {
    BOOST_LOG_TRIVIAL(info) << "Exiting Ground Safe State.";
    
    return STATE_GROUND_SAFE;
}

uint32_t groundSafeStateInit(enum STATES (*canParseFunctions[CANIDS_EXTENDED_MAX]) (can_frame *)) {
    canParseFunctions[CANIDS_EXTENDED_STATE_ENTER] = groundSafeStateEnter;
    canParseFunctions[CANIDS_EXTENDED_STATE_EXIT] = groundSafeStateExit;

    canParseFunctions[CANIDS_HELIUM_PRESSURE_PT_DATA] = parseHeliumPressurePTData;

    return 0;
}
