#ifndef LEAK_CHECK_H_
#define LEAK_CHECK_H_

#include "CANIDs.h"

/**
 * @defgroup leakCheckGroup Leak Check
 * @brief Unique CAN message parsing for the leak check state.
 * 
 * @{
 */

uint32_t leakCheckExit();
uint32_t leakCheckInit(uint32_t (*canParseFunctions[CANIDS_MAX_CANID]) (can_frame *));

/**
 * @} leakCheckGroup
 */

#endif // LEAK_CHECK_H_