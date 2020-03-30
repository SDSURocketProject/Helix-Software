#include "event.h"
#include <iostream>
#include <thread>
#include <chrono>
#include <boost/log/trivial.hpp>
#include "Helix-OBC-Firmware.h"

uint32_t canParseNothing(can_frame *data) {
    BOOST_LOG_TRIVIAL(info) << "canParseNothing called with id " << data->can_id;
    return 0;
}

// A 2d array containing function pointers for each canID for each possible state
static enum STATES (*canParseFunctions[STATE_MAX_STATES][CANIDS_EXTENDED_MAX]) (can_frame *);
// An array of function pointers for default processing of canIDs
static uint32_t (*canParseFunctionsDefault[CANIDS_EXTENDED_MAX]) (can_frame *);

static uint32_t checkInitFunction(enum STATES state, std::string stateName, uint32_t result) {
    if (result > 0) {
        BOOST_LOG_TRIVIAL(error) << stateName << " init Error";
        return 1;
    }
    else if (canParseFunctions[state][CANIDS_EXTENDED_STATE_ENTER] == nullptr) {
        BOOST_LOG_TRIVIAL(error) << stateName << " state enter callback not initialized";
        return 1;
    }
    else if (canParseFunctions[state][CANIDS_EXTENDED_STATE_EXIT] == nullptr) {
        BOOST_LOG_TRIVIAL(error) << stateName << " state exit callback not initialized";
        return 1;
    }
    else {
        BOOST_LOG_TRIVIAL(info) << stateName << " CAN parser init completed without error.";
        return 0;
    }
}

void eventParse(bounded_buffer<struct can_frame>& thing) {
    uint32_t result = 0;

    BOOST_LOG_TRIVIAL(trace) << "Start event thread";

    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    // Set default parsing functions
    for (uint32_t canID = 0; canID < CANIDS_EXTENDED_MAX; canID++) {
        canParseFunctionsDefault[canID] = canParseNothing;
    }

    // Use default parsing for can messages
    for (uint32_t state = STATE_IDLE; state < STATE_MAX_STATES; state++) {
        for (uint32_t canID = 0; canID < CANIDS_EXTENDED_MAX; canID++) {
            canParseFunctions[state][canID] = NULL;
        }
    }

    result = leakCheckInit(canParseFunctions[STATE_LEAK_CHECK]);
    result = checkInitFunction(STATE_LEAK_CHECK, "Leak check", result);
    if (result != 0) {
        // exit?
    }
    
    struct can_frame item;
    enum STATES currentState = STATE_LEAK_CHECK;
    enum STATES nextState = STATE_LEAK_CHECK;

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
            canParseFunctionsDefault[item.can_id](&item);
        }
        else {
            nextState = canParseFunctions[currentState][item.can_id](&item);
        }
        if (nextState != currentState) {
            canParseFunctions[currentState][CANIDS_EXTENDED_STATE_EXIT](nullptr);
            canParseFunctions[nextState][CANIDS_EXTENDED_STATE_ENTER](nullptr);
            currentState = nextState;
        }
    }
}

