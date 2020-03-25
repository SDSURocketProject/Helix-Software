#include "event.h"
#include <iostream>
#include <thread>
#include <chrono>
#include <boost/log/trivial.hpp>


uint32_t canParseNothing(can_frame *data) {
    BOOST_LOG_TRIVIAL(info) << "canParseNothing called";
    return 0;
}

// A 2d array containing function pointers for each canID for each possible state
static uint32_t (*canParseFunctions[STATE_MAX_STATES][CANIDS_MAX_CANID]) (can_frame *);
// An array of function pointers for default processing of canIDs
static uint32_t (*canParseFunctionsDefault[CANIDS_MAX_CANID]) (can_frame *);

void eventParse(bounded_buffer<struct can_frame>& thing) {
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    // Set default parsing functions
    for (int canID = 0; canID < CANIDS_MAX_CANID; canID++) {
        canParseFunctionsDefault[canID] = canParseNothing;
    }

    // Use default parsing for can messages
    for (int state = 0; state < STATE_MAX_STATES; state++) {
        for (int canID = 0; canID < CANIDS_MAX_CANID; canID++) {
            canParseFunctions[state][canID] = NULL;
        }
    }
    

    if (leakCheckInit(canParseFunctions[STATE_LEAK_CHECK]) > 0) {
        BOOST_LOG_TRIVIAL(error) << "Leak Check init Error";
    }
    else {
        BOOST_LOG_TRIVIAL(info) << "Leak Check CAN parser init completed without error.";
    }

    struct can_frame item;
    uint32_t currentState = STATE_LEAK_CHECK;
    uint32_t nextState;

    while (item.can_id != CANIDS_QUIT) {
        thing.pop_back(&item);
        if (item.can_id & CAN_EFF_FLAG) {
            // EFF/SFF is set in the MSB
        }
        else if (item.can_id & CAN_RTR_FLAG) {
            // remote transmission request
        }
        else if (item.can_id & CAN_ERR_FLAG) {
            // error message frame
            continue;
        }


        if (canParseFunctions[currentState][item.can_id] == NULL) {
            nextState = canParseFunctionsDefault[item.can_id](&item);
        }
        else {
            nextState = canParseFunctions[currentState][item.can_id](&item);
        }
        if (nextState != currentState) {
            // Handle generic state change
        }
    }
}

