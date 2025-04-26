#!/usr/bin/env python3
from datetime import datetime, date

# --- TOU Rates ($/kWh) ---
WINTER_OFF_PEAK = 0.076
WINTER_MID_PEAK = 0.122
WINTER_ON_PEAK  = 0.158

SUMMER_OFF_PEAK = 0.074
SUMMER_ON_PEAK  = 0.151
SUMMER_MID_PEAK = 0.102

# --- ULO Rates ($/kWh) ---
ULO_ULTRA_LOW        = 0.028
ULO_WEEKEND_OFF_PEAK = 0.076
ULO_MID_PEAK         = 0.122
ULO_ON_PEAK          = 0.284

# ANSI color codes
GREEN  = '\033[32m'
YELLOW = '\033[33m'
RED    = '\033[31m'
RESET  = '\033[0m'

def electricity_rate(dt=None, holidays=None, schedule='TOU'):
    if dt is None:
        dt = datetime.now()
    if holidays is None:
        holidays = set()
    is_weekday = (dt.weekday() < 5) and (dt.date() not in holidays)
    is_weekend = not is_weekday
    hour = dt.hour + dt.minute/60.0
    month = dt.month
    is_winter = (month >= 11 or month <= 4)

    if schedule.upper() == 'TOU':
        if not is_weekday or hour < 7 or hour >= 19:
            return WINTER_OFF_PEAK if is_winter else SUMMER_OFF_PEAK
        if is_winter:
            return WINTER_MID_PEAK if 11 <= hour < 17 else WINTER_ON_PEAK
        return SUMMER_ON_PEAK if 11 <= hour < 17 else SUMMER_MID_PEAK
    elif schedule.upper() == 'ULO':
        if hour >= 23 or hour < 7:
            return ULO_ULTRA_LOW
        if is_weekend:
            return ULO_WEEKEND_OFF_PEAK
        if (7 <= hour < 16) or (21 <= hour < 23):
            return ULO_MID_PEAK
        return ULO_ON_PEAK
    else:
        raise ValueError("Unknown schedule")

def color_rate(rate, schedule='TOU'):
    sched = schedule.upper()
    if sched == 'ULO':
        if rate in (ULO_ULTRA_LOW, ULO_WEEKEND_OFF_PEAK):
            color = GREEN
        else:
            color = RED
        return f"{color}${rate:.3f}{RESET}"
    if rate in (WINTER_OFF_PEAK, SUMMER_OFF_PEAK):
        color = GREEN
    elif rate in (WINTER_MID_PEAK, SUMMER_MID_PEAK):
        color = YELLOW
    else:
        color = RED
    return f"{color}${rate:.3f}{RESET}"

def rate_level_box(dt=None, holidays=None, schedule='TOU'):
    # Colored ASCII [BOX] indicator
    rate = electricity_rate(dt, holidays, schedule)
    sched = schedule.upper()
    # ULO: green for best (ultra-low & weekend), red otherwise
    if sched == 'ULO':
        return GREEN + "[BOX]" + RESET if rate in (ULO_ULTRA_LOW, ULO_WEEKEND_OFF_PEAK) else RED + "[BOX]" + RESET
    # TOU: green/yellow/red for off/mid/on
    if rate in (WINTER_OFF_PEAK, SUMMER_OFF_PEAK):
        return GREEN + "[BOX]" + RESET
    if rate in (WINTER_MID_PEAK, SUMMER_MID_PEAK):
        return YELLOW + "[BOX]" + RESET
    return RED + "[BOX]" + RESET

def load_rate_icon(dt=None, holidays=None, schedule='TOU'):
    rate = electricity_rate(dt, holidays, schedule)
    sched = schedule.upper()
    if sched == 'ULO':
        return 'green.gif' if rate in (ULO_ULTRA_LOW, ULO_WEEKEND_OFF_PEAK) else 'red.gif'
    if rate in (WINTER_OFF_PEAK, SUMMER_OFF_PEAK):
        return 'green.gif'
    if rate in (WINTER_MID_PEAK, SUMMER_MID_PEAK):
        return 'yellow.gif'
    return 'red.gif'

if __name__ == "__main__":
    holidays = {date(2025,1,1), date(2025,12,25)}
    tests = [
        datetime(2025,1,15,8,30),
        datetime(2025,1,15,12,0),
        datetime(2025,1,18,14,0),
        datetime(2025,5,15,8,30),
        datetime(2025,5,15,12,0),
        datetime(2025,5,17,20,0),
        datetime(2025,6,10,23,30),
        datetime(2025,6,11,6,45),
    ]
    for sched in ('TOU','ULO'):
        print(f"--- {sched} Tests ---")
        for dt in tests:
            rate = electricity_rate(dt,holidays,sched)
            print(f"{dt:%Y-%m-%d %a %H:%M} -> {color_rate(rate,sched)} {rate_level_box(dt,holidays,sched)} {load_rate_icon(dt,holidays,sched)}")
    print("--- Current Time ---")
    for sched in ('TOU','ULO'):
        rate = electricity_rate(schedule=sched)
        print(f"{sched} now -> {color_rate(rate,sched)} {rate_level_box(schedule=sched)} {load_rate_icon(schedule=sched)}")
