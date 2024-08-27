'''
Home Assistant integration for Imeon Inverters
---
Rodrigue Lemaire
---
July 2024
'''

from voluptuous import All, Range, In

def list_keys(dictn: dict, type: str) -> list:
    """Return a list of keys of items with a given 'type' field."""
    result = []
    for k,v in dictn.items():
        if v["type"]==type: result.append(k)
    return result

# Sensors & Text Entities
GET_REQUESTS = {
    # Battery
    "battery_autonomy": {'type': 'number', 'friendly_name': 'Battery Autonomy', 'unit': ''},
    "battery_charge_time": {'type': 'number', 'friendly_name': 'Battery Charge Time', 'unit': ''},
    "battery_power": {'type': 'number', 'friendly_name': 'Battery Power', 'unit': 'W'},
    "battery_soc": {'type': 'number', 'friendly_name': 'Battery SOC', 'unit': '%'},
    "battery_status": {'type': 'text', 'friendly_name': 'Battery Status'},
    "battery_stored": {'type': 'number', 'friendly_name': 'Battery Stored', 'unit': 'Wh'},

    # Grid
    "grid_current_l1": {'type': 'number', 'friendly_name': 'Grid Current L1', 'unit': 'A'},
    "grid_current_l2": {'type': 'number', 'friendly_name': 'Grid Current L2', 'unit': 'A'},
    "grid_current_l3": {'type': 'number', 'friendly_name': 'Grid Current L3', 'unit': 'A'},
    "grid_frequency": {'type': 'number', 'friendly_name': 'Grid Frequency', 'unit': 'Hz'},
    "grid_voltage_l1": {'type': 'number', 'friendly_name': 'Grid Voltage L1', 'unit': 'V'},
    "grid_voltage_l2": {'type': 'number', 'friendly_name': 'Grid Voltage L1', 'unit': 'V'},
    "grid_voltage_l3": {'type': 'number', 'friendly_name': 'Grid Voltage L1', 'unit': 'V'},

    # AC Input
    "input_power_l1": {'type': 'number', 'friendly_name': 'Input Power L1', 'unit': 'W'},
    "input_power_l2": {'type': 'number', 'friendly_name': 'Input Power L2', 'unit': 'W'},
    "input_power_l3": {'type': 'number', 'friendly_name': 'Input Power L3', 'unit': 'W'},
    "input_power_total": {'type': 'number', 'friendly_name': 'Input Power Total', 'unit': 'W'},

    # Inverter settings
    "inverter_charging-current-limit": {'type': 'number', 'friendly_name': 'Charging Current Limit', 'unit': 'A'},
    "inverter_injection-power-limit": {'type': 'number', 'friendly_name': 'Injection Power Limit', 'unit': 'W'},
    "inverter_inverter": {'type': 'text', 'friendly_name': 'Inverter Model'},
    "inverter_serial": {'type': 'text', 'friendly_name': 'Inverter Serial Number'},
    "inverter_software": {'type': 'text', 'friendly_name': 'Inverter Software Version'},
    "inverter_battery_grid_charge": {'type': 'text', 'friendly_name': 'Battery Grid Charge'},
    "inverter_battery_night_discharge": {'type': 'text', 'friendly_name': 'Battery Night Discharge'},

    # Manager settings
    "manager_inverter_mode": {'type': 'text', 'friendly_name': 'Inverter Mode'},
    "manager_inverter_state": {'type': 'text', 'friendly_name': 'Inverter State'},
    "manager_relay_check": {'type': 'text', 'friendly_name': 'Relay Check'},
    "manager_relay_state": {'type': 'text', 'friendly_name': 'Relay State'},
    "manager_lcd_sleep_time": {'type': 'text', 'friendly_name': 'LCD Screen Sleep Time'},

    # Electric Meter
    "meter_active": {'type': 'text', 'friendly_name': 'Meter Active'},
    "meter_power": {'type': 'number', 'friendly_name': 'Meter Power', 'unit': 'W'},
    "meter_power_protocol": {'type': 'number', 'friendly_name': 'Meter Power Protocol', 'unit': 'W'},

    # AC Output
    "output_current_l1": {'type': 'number', 'friendly_name': 'Output Current L1', 'unit': 'A'},
    "output_current_l2": {'type': 'number', 'friendly_name': 'Output Current L2', 'unit': 'A'},
    "output_current_l3": {'type': 'number', 'friendly_name': 'Output Current L3', 'unit': 'A'},
    "output_frequency": {'type': 'number', 'friendly_name': 'Output Frequency', 'unit': 'Hz'},
    "output_power_l1": {'type': 'number', 'friendly_name': 'Output Power L1', 'unit': 'W'},
    "output_power_l2": {'type': 'number', 'friendly_name': 'Output Power L2', 'unit': 'W'},
    "output_power_l3": {'type': 'number', 'friendly_name': 'Output Power L3', 'unit': 'W'},
    "output_power_total": {'type': 'number', 'friendly_name': 'Output Power Total', 'unit': 'W'},
    "output_voltage_l1": {'type': 'number', 'friendly_name': 'Output Voltage L1', 'unit': 'V'},
    "output_voltage_l2": {'type': 'number', 'friendly_name': 'Output Voltage L2', 'unit': 'V'},
    "output_voltage_l3": {'type': 'number', 'friendly_name': 'Output Voltage L3', 'unit': 'V'},

    # Solar Panel
    "pv_consumed": {'type': 'number', 'friendly_name': 'PV Consumed', 'unit': 'Wh'},
    "pv_injected": {'type': 'number', 'friendly_name': 'PV Injected', 'unit': 'Wh'},
    "pv_power_1": {'type': 'number', 'friendly_name': 'PV Power 1', 'unit': 'W'},
    "pv_power_2": {'type': 'number', 'friendly_name': 'PV Power 2', 'unit': 'W'},
    "pv_power_total": {'type': 'number', 'friendly_name': 'PV Power Total', 'unit': 'W'},
    #"pv_stored": {'type': 'number', 'friendly_name': 'PV Stored', 'unit': ''}, # Avoid, confusing entry
    
    # Temperature
    "temp_air_temperature": {'type': 'number', 'friendly_name': 'Air Temperature', 'unit': '°C'},
    "temp_component_temperature": {'type': 'number', 'friendly_name': 'Component Temperature', 'unit': '°C'},

    # Monitoring (data over the last 24 hours)
    "monitoring_building_consumption": {'type': 'number', 'friendly_name': 'Monitoring Building Consumption', 'unit': 'Wh'},
    "monitoring_economy_factor": {'type': 'number', 'friendly_name': 'Monitoring Economy Factor', 'unit': ''},
    "monitoring_grid_consumption": {'type': 'number', 'friendly_name': 'Monitoring Grid Consumption', 'unit': 'Wh'},
    "monitoring_grid_injection": {'type': 'number', 'friendly_name': 'Monitoring Grid Injection', 'unit': 'Wh'},
    "monitoring_grid_power_flow": {'type': 'number', 'friendly_name': 'Monitoring Grid Power Flow', 'unit': 'Wh'},
    "monitoring_self_consumption": {'type': 'number', 'friendly_name': 'Monitoring Self Consumption', 'unit': '%'},
    "monitoring_self_sufficiency": {'type': 'number', 'friendly_name': 'Monitoring Self Suffiency', 'unit': '%'},
    "monitoring_solar_production": {'type': 'number', 'friendly_name': 'Monitoring Solar Production', 'unit': 'Wh'},

    # Monitoring (instant minute data)
    "monitoring_minute_building_consumption": {'type': 'number', 'friendly_name': 'Monitoring Building Consumption (minute)', 'unit': 'W'},
    #"monitoring_minute_economy_factor": {'type': 'number', 'friendly_name': 'Monitoring Economy Factor (minute)', 'unit': ''},
    "monitoring_minute_grid_consumption": {'type': 'number', 'friendly_name': 'Monitoring Grid Consumption (minute)', 'unit': 'W'},
    "monitoring_minute_grid_injection": {'type': 'number', 'friendly_name': 'Monitoring Grid Injection (minute)', 'unit': 'W'},
    "monitoring_minute_grid_power_flow": {'type': 'number', 'friendly_name': 'Monitoring Grid Power Flow (minute)', 'unit': 'W'},
    #"monitoring_minute_self_consumption": {'type': 'number', 'friendly_name': 'Monitoring Self Consumption (minute)', 'unit': '%'},
    #"monitoring_minute_self_sufficiency": {'type': 'number', 'friendly_name': 'Monitoring Self Suffiency (minute)', 'unit': '%'},
    "monitoring_minute_solar_production": {'type': 'number', 'friendly_name': 'Monitoring Solar Production (minute)', 'unit': 'W'},
}

# Services
POST_REQUESTS = {
    "inverter_mode":    {"friendly_name": 'Inverter Mode',
                         "description": 'Change the mode of the inverter.',
                            "fields": {
                                "mode": {"type": All(str, In(['smg', 'bup', 'ong', 'ofg'])), "example": 'smg'}
                                }
                        },
    "mppt":             {"friendly_name": 'Maximum Power Point Tracking Range',
                         "description": 'Change the working range of the MPPT.',
                            "fields": {
                                "low": {"type": All(int, Range(min=350)), "example": 350},
                                "high": {"type": All(int, Range(max=700)), "example": 700}
                                }
                        },
    "feed_in":          {"friendly_name": 'Grid Feed-in (Injection)',
                         "description": 'Change whether or not the inverter injects power into the grid.',
                            "fields": {
                                "active": {"type": All(bool), "example": True},
                                }
                        },
    "injection_power":  {"friendly_name": 'Injection Power Limit',
                         "description": 'Change the power limit when injecting into the grid.',
                            "fields": {
                                "limit": {"type": All(int, Range(min=0,max=8000)), "example": 3000},
                                }
                        },
    "lcd_time":         {"friendly_name": 'LCD Screen Sleep Time',
                         "description": 'Change the time it takes for the LCD screen to go to sleep.',
                            "fields": {
                                "time": {"type": All(int, In([0, 1, 2, 10, 20])), "example": 0},
                                }
                        },
    "night_discharge":  {"friendly_name": 'Battery Night Discharge',
                         "description": 'Change whether or not the battery should discharge at night.',
                            "fields": {
                                "active": {"type": All(bool), "example": False, "values": [True, False]},
                                }
                        },
    "grid_charge":      {"friendly_name": 'Battery Charge From Grid',
                         "description": 'Change whether or not the battery should charge from the grid.',
                            "fields": {
                                "active": {"type": All(bool), "example": False, "values": [True, False]},
                                }
                        },
    "relay":            {"friendly_name": 'Relay State',
                         "description": 'Change the state of the relay.',
                            "fields": {
                                "active": {"type": All(bool), "example": False, "values": [True, False]},
                                }
                        },
    "ac_output":        {"friendly_name": 'AC Output State',
                         "description": 'Change whether or not the AC output should be active.',
                            "fields": {
                                "active": {"type": All(bool), "example": True, "values": [True, False]},
                                }
                        }
}

LIST_TEXT  = list_keys(GET_REQUESTS, 'text')
LIST_FLOAT = list_keys(GET_REQUESTS, 'number')

# Icons for Logbook entries
TIMELINE_WARNINGS = {
    'com_lost': 'mdi:lan-disconnect',
    'com_ok': 'mdi:lan-connect',
    'warning_grid': 'mdi:alert-circle',
    'warning_ond': 'mdi:alert-circle',
    'warning_soft': 'mdi:alert-circle',
    'warning_pv': 'mdi:alert-circle',
    'warning_bat': 'mdi:alert-circle',
    'warning_cpu': 'mdi:alert-circle',
    'warning_spe': 'mdi:alert-circle',
    'error_grid': 'mdi:close-octagon',
    'error_ond': 'mdi:close-octagon',
    'error_soft': 'mdi:close-octagon',
    'error_pv': 'mdi:close-octagon',
    'error_bat': 'mdi:close-octagon',
    'error_spe': 'mdi:close-octagon-outline',
    'info_grid': 'mdi:information-slab-circle',
    'info_ond': 'mdi:information-slab-circle',
    'info_soft': 'mdi:information-slab-circle',
    'info_pv': 'mdi:information-slab-circle',
    'info_bat': 'mdi:information-slab-circle',
    'info_cpu': 'mdi:information-slab-circle',
    'info_spe': 'mdi:information-slab-circle',
    'warning_???': 'mdi:alert',
    'warnings': 'mdi:alert',
    'error_???': 'mdi:close-octagon',
    'errors': 'mdi:close-octagon',
    'good_1': 'mdi:check-circle',
    'good_2': 'mdi:check-circle',
    'good_3': 'mdi:check-circle',
}