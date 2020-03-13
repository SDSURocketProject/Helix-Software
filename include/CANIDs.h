// WARNING START OF SECTION AUTOGENERATED BY PYTHON SCRIPT
// THIS SECTION MAY BE AUTOMATICALLY CHANGED AT ANY TIME
// Autogenerated section name: CAN Config
// File path of script: ARD/genCAN.py
#ifndef CANIDS_H_
#define CANIDS_H_

#include <linux/can.h>
#include <stdint.h>

enum STATES {
	STATE_IDLE,
	STATE_DEBUG,
	STATE_DRY_SYSTEMS,
	STATE_LEAK_CHECK,
	STATE_FUELING,
	STATE_LAUNCH,
	STATE_STAGE_TWO,
	STATE_RECOVERY,
	STATE_GROUND_SAFE,
	STATE_FLIGHT_SAFE,
	STATE_MAX_STATES
};

enum CANIDs : uint32_t {
	CANIDS_CLOCK_SYNC = 0UL,
	CANIDS_EMERGENCY_SIGNAL = 1UL,
	CANIDS_HELIUM_PRESSURE_PT_DATA = 100UL,
	CANIDS_LOX_PRESSURE_PT_DATA = 101UL,
	CANIDS_METHANE_PRESSURE_PT_DATA = 102UL,
	CANIDS_CHAMBER_PRESSURE_PT_DATA = 103UL,
	CANIDS_HELIUM_FILL_VALVE_HALL_EFFECT_STATE = 200UL,
	CANIDS_LOX_FILL_VALVE_HALL_EFFECT_STATE = 201UL,
	CANIDS_METHANE_FILL_VALVE_HALL_EFFECT_STATE = 202UL,
	CANIDS_HELIUM_TANK_TEMPERATURE_DATA = 300UL,
	CANIDS_LOX_TANK_TEMPERATURE_DATA = 301UL,
	CANIDS_METHANE_TANK_TEMPERATURE_DATA = 302UL,
	CANIDS_NOZZLE_TEMPERATURE_DATA = 303UL,
	CANIDS_UPPER_AIR_FRAME_TEMPERATURE_DATA = 304UL,
	CANIDS_HELIUM_PRESSURE_PT_CURRENT = 400UL,
	CANIDS_LOX_PRESSURE_PT_CURRENT = 401UL,
	CANIDS_METHANE_PRESSURE_PT_CURRENT = 402UL,
	CANIDS_CHAMBER_PRESSURE_PT_CURRENT = 403UL,
	CANIDS_HELIUM_FILL_VALVE_HALL_EFFECT_CURRENT = 404UL,
	CANIDS_LOX_FILL_VALVE_HALL_EFFECT_CURRENT = 405UL,
	CANIDS_METHANE_FILL_VALVE_HALL_EFFECT_CURRENT = 406UL,
	CANIDS_UPPER_AIR_FRAME_VIN_CURRENT = 407UL,
	CANIDS_UPPER_AIR_FRAME_VIN_VOLTAGE = 500UL,
	CANIDS_MAX_CANID
};

struct clock_sync {
	uint32_t utc_time;
};

struct emergency_signal {
	uint8_t status;
};

struct helium_pressure_pt_data {
	uint32_t utc_time;
	uint16_t helium_pressure;
};

struct lox_pressure_pt_data {
	uint32_t utc_time;
	uint16_t lox_pressure;
};

struct methane_pressure_pt_data {
	uint32_t utc_time;
	uint16_t methane_pressure;
};

struct chamber_pressure_pt_data {
	uint32_t utc_time;
	uint16_t chamber_pressure;
};

struct helium_fill_valve_hall_effect_state {
	uint32_t utc_time;
	uint8_t helium_fill_valve_hall_effect_state;
};

struct lox_fill_valve_hall_effect_state {
	uint32_t utc_time;
	uint8_t lox_fill_valve_hall_effect_state;
};

struct methane_fill_valve_hall_effect_state {
	uint32_t utc_time;
	uint8_t methane_fill_valve_hall_effect_state;
};

struct helium_tank_temperature_data {
	uint32_t utc_time;
	int16_t helium_tank_temperature;
};

struct lox_tank_temperature_data {
	uint32_t utc_time;
	int16_t lox_tank_temperature;
};

struct methane_tank_temperature_data {
	uint32_t utc_time;
	int16_t methane_tank_temperature;
};

struct nozzle_temperature_data {
	uint32_t utc_time;
	int16_t nozzle_temperature;
};

struct upper_air_frame_temperature_data {
	uint32_t utc_time;
	int16_t upper_air_frame_temperature;
};

struct helium_pressure_pt_current {
	uint32_t utc_time;
	int16_t helium_pressure_pt_current;
};

struct lox_pressure_pt_current {
	uint32_t utc_time;
	int16_t lox_pressure_pt_current;
};

struct methane_pressure_pt_current {
	uint32_t utc_time;
	int16_t methane_pressure_pt_current;
};

struct chamber_pressure_pt_current {
	uint32_t utc_time;
	int16_t chamber_pressure_pt_current;
};

struct helium_fill_valve_hall_effect_current {
	uint32_t utc_time;
	int16_t helium_fill_valve_hall_effect_current;
};

struct lox_fill_valve_hall_effect_current {
	uint32_t utc_time;
	int16_t lox_fill_valve_hall_effect_current;
};

struct methane_fill_valve_hall_effect_current {
	uint32_t utc_time;
	int16_t methane_fill_valve_hall_effect_current;
};

struct upper_air_frame_vin_current {
	uint32_t utc_time;
	int16_t upper_air_frame_board_current;
};

struct upper_air_frame_vin_voltage {
	uint32_t utc_time;
	int16_t upper_air_frame_board_vin_voltage;
};

#endif // CANIDS_H_
// WARNING END OF SECTION AUTOGENERATED BY PYTHON SCRIPT
// THIS SECTION MAY BE AUTOMATICALLY CHANGED AT ANY TIME
// Autogenerated section name: CAN Config
// File path of script: ARD/genCAN.py
