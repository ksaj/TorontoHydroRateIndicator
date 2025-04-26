#!/usr/bin/env python3
from datetime import datetime, date

# --- TOU Rates ($/kWh) ---
WINTER_OFF_PEAK = 0.076   # 7.6¢
WINTER_MID_PEAK = 0.122   # 12.2¢
WINTER_ON_PEAK  = 0.158   # 15.8¢

SUMMER_OFF_PEAK = 0.074   # 7.4¢
SUMMER_ON_PEAK  = 0.151   # 15.1¢
SUMMER_MID_PEAK = 0.102   # 10.2¢

# --- ULO Rates ($/kWh) ---
ULO_ULTRA_LOW         = 0.028   # 2.8¢
ULO_WEEKEND_OFF_PEAK  = 0.076   # 7.6¢
ULO_MID_PEAK          = 0.122   # 12.2¢
ULO_ON_PEAK           = 0.284   # 28.4¢

# ANSI color codes (for terminal output)
GREEN  = '\033[32m'
YELLOW = '\033[33m'
RED    = '\033[31m'
RESET  = '\033[0m'


def electricity_rate(dt=None, holidays=None, schedule='TOU'):
    """
    Return the rate (in $/kWh) for the given datetime & schedule.
    If dt is None, uses the current date and time.
    schedule: 'TOU' or 'ULO'
    """
    if dt is None:
        dt = datetime.now()
    if holidays is None:
        holidays = set()

    is_weekday = (dt.weekday() < 5) and (dt.date() not in holidays)
    is_weekend_or_holiday = not is_weekday
    hour = dt.hour + dt.minute / 60.0
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
        if is_weekend_or_holiday:
            return ULO_WEEKEND_OFF_PEAK
        if (7 <= hour < 16) or (21 <= hour < 23):
            return ULO_MID_PEAK
        return ULO_ON_PEAK

    else:
        raise ValueError(f"Unknown schedule: {schedule!r}")


def color_rate(rate, schedule='TOU'):
    """Wrap the rate in ANSI color based on its level and schedule."""
    sched = schedule.upper()
    if sched == 'ULO':
        # Only green for best times (ultra-low & weekend off-peak), red otherwise
        if rate in (ULO_ULTRA_LOW, ULO_WEEKEND_OFF_PEAK):
            color = GREEN
        else:
            color = RED
        return f"{color}${rate:.3f}{RESET}"

    # TOU coloring: green, yellow, red
    if rate in (WINTER_OFF_PEAK, SUMMER_OFF_PEAK):
        color = GREEN
    elif rate in (WINTER_MID_PEAK, SUMMER_MID_PEAK):
        color = YELLOW
    else:
        color = RED
    return f"{color}${rate:.3f}{RESET}"


def rate_level_box(dt=None, holidays=None, schedule='TOU'):
    """
    Return a single colored box (■) indicating the rate level:
      - For ULO: green for ultra-low & weekend off-peak, red otherwise
      - For TOU: green for off-peak, yellow for mid-peak, red for on-peak
    """
    rate = electricity_rate(dt, holidays, schedule)
    sched = schedule.upper()

    if sched == 'ULO':
        # Green only for ultra-low or weekend off-peak
        if rate in (ULO_ULTRA_LOW, ULO_WEEKEND_OFF_PEAK):
            return GREEN + '■' + RESET
        return RED + '■' + RESET

    # TOU logic
    if rate in (WINTER_OFF_PEAK, SUMMER_OFF_PEAK):
        return GREEN + '■' + RESET
    if rate in (WINTER_MID_PEAK, SUMMER_MID_PEAK):
        return YELLOW + '■' + RESET
    return RED + '■' + RESET


def load_rate_icon(dt=None, holidays=None, schedule='TOU'):
    """
    Return the filename of a GIF icon for the rate level:
      - For ULO: 'green.gif' for ultra-low & weekend off-peak, 'red.gif' otherwise
      - For TOU: 'green.gif', 'yellow.gif', or 'red.gif'
    """
    rate = electricity_rate(dt, holidays, schedule)
    sched = schedule.upper()

    if sched == 'ULO':
        if rate in (ULO_ULTRA_LOW, ULO_WEEKEND_OFF_PEAK):
            return 'green.gif'
        return 'red.gif'

    # TOU icon mapping
    if rate in (WINTER_OFF_PEAK, SUMMER_OFF_PEAK):
        return 'green.gif'
    if rate in (WINTER_MID_PEAK, SUMMER_MID_PEAK):
        return 'yellow.gif'
    return 'red.gif'


if __name__ == "__main__":
    # Holiday definitions
    holidays = {date(2025, 1, 1), date(2025, 12, 25)}
    # Sample datetimes for tests
    tests = [
        datetime(2025, 1, 15, 8, 30),   # winter on-peak
        datetime(2025, 1, 15, 12, 0),   # winter mid-peak
        datetime(2025, 1, 18, 14, 0),   # winter off-peak
        datetime(2025, 5, 15, 8, 30),   # summer mid-peak
        datetime(2025, 5, 15, 12, 0),   # summer on-peak
        datetime(2025, 5, 17, 20, 0),   # summer off-peak
        datetime(2025, 6, 10, 23, 30),  # ULO ultra-low overnight
        datetime(2025, 6, 11,  6, 45),  # ULO ultra-low overnight
    ]

    for sched in ('TOU', 'ULO'):
        print(f"\n--- {sched} Schedule Tests ---")
        for dt in tests:
            rate = electricity_rate(dt, holidays, sched)
            colored = color_rate(rate, sched)
            box = rate_level_box(dt, holidays, sched)
            icon = load_rate_icon(dt, holidays, sched)
            print(f"{dt:%Y-%m-%d %a %H:%M} → {colored} {box} {icon}/kWh")

    # Now tests without explicit dt (current time)
    print(f"\n--- Current Time Tests ---")
    for sched in ('TOU', 'ULO'):
        rate = electricity_rate(schedule=sched)
        print(f"{sched} now → {color_rate(rate, sched)} {rate_level_box(schedule=sched)} {load_rate_icon(schedule=sched)}")

