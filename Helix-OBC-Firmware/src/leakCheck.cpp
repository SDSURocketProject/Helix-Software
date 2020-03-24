#include "leakCheck.h"
#include "eventTimer.h"
#include <iostream>

#include <thread>
#include <chrono>

/**
 * @addtogroup stateLeakCheckGroup
 * @{
 * 
 * @cond COMPILING_LATEX
 * @verbatim
 * 
 * \subsection{Custom Leak Check Actions}
 * 
 * @endverbatim
 * @endcond
 */

/**
 * @brief Parses Helium Pressure PT Data when received over the CAN Bus and in the leak check state.
 * @param[in] *data Contains the Helium Pressure PT Data CAN bus frame
 * @return Returns the state to move into
 * 
 * @cond COMPILING_LATEX
 * @verbatim CANID_DEF (Helium Pressure PT Data) @endverbatim
 * 
 * @endcond
 * 
 * @retval STATE_LEAK_CHECK Continue in the leak check state.
 * @retval STATE_IDLE Finished leak check so return to the idle state.
 * @retval STATE_GROUND_SAFE Return to the ground safe state because the helium tank pressure is overpressurized.
 * 
 * @cond COMPILING_LATEX
 * 
 * When Helium Pressure PT Data is received the CANID will be printed to stdout and the data will
 * be printed as a string to stdout. The current time and data with milliseconds is then printed
 * to stdout. The received can_frame is added to the eventTimer so that the received frame will
 * be receved again in 1 second. The system then continues on in the leak check state.
 * 
 * @verbatim END_CANID_DEF @endverbatim
 * 
 * @endcond
 * \n
 * The following will be done when Helium Pressure PTData is received while in the leak check state:
 * \n
 */
uint32_t parseHeliumPressurePTData(can_frame *data) {
    //struct helium_pressure_pt_data *pressurePTData = data;
    //! Print out CANID and Data from the can_frame
    std::cout << "CANID: " << data->can_id << "\n";
    std::cout << "Data: " << data->data << "\n";

    //! Print out the current time with milliseconds
    std::chrono::system_clock::time_point p = std::chrono::system_clock::now();

    std::chrono::milliseconds ms = std::chrono::duration_cast<std::chrono::milliseconds>(p.time_since_epoch());
    std::chrono::seconds s = std::chrono::duration_cast<std::chrono::seconds>(ms);
    std::time_t t = s.count();
    std::size_t fracSeconds = ms.count() % 1000;
    std::cout << "Time: " << std::ctime(&t) << " " << fracSeconds << "\n";

    //! Send this can_frame again in seconds
    eventTimerPushEvent(data, 1000);

    //! Continue in the leak check state.
    return STATE_LEAK_CHECK;
}

/**
 * @brief Called when entering the leak check state
 * @return Returns 0.
 * 
 * Prints a warning to stdout that the system is entering the leak check state.
 */
uint32_t leakCheckEnter() {
    std::cout << "Starting Leak Check.\n";
    return 0;
}

/**
 * @brief Called when exiting the leak check state
 * @return Returns 0.
 * 
 * Prints a warning to stdout that the system is exiting the leak check state.
 */
uint32_t leakCheckExit() {
    std::cout << "Exiting Leak Check.\n";
    return 0;
}

/**
 * @brief Initialize leak check can parsing functions prior to starting event system
 * @param[out] *canParseFunctions List of pointers to functions that will be called when the associated CAN message is received.
 * 
 * The CAN Bus messages that need to be parsed uniquely to the leak check state are assigned to the canParse Functions array.
 */
uint32_t leakCheckInit(uint32_t (*canParseFunctions[CANIDS_MAX_CANID]) (can_frame *)) {
    canParseFunctions[CANIDS_HELIUM_PRESSURE_PT_DATA] = parseHeliumPressurePTData;
    canParseFunctions[CANIDS_LOX_PRESSURE_PT_DATA] = parseHeliumPressurePTData;

    return 0;
}

/**
 * @} stateLeakCheckGroup
 */
