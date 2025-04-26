# Toronto Hydro Rate Calculator — HOWTO.md

This guide explains the **Time‑Of‑Use (TOU)** and **Ultra‑Low Overnight (ULO)** electricity rate structures used by Toronto Hydro, and shows you how to call the Python functions to retrieve rates, colored output, and icon filenames.  

> **Note:** Toronto Hydro also has a volumetric threshold at **1,000 kWh** per billing period, but that applies only to very high‑consuming operations (e.g. grow‑ops, large server farms). This calculator is designed for regular households, so the threshold is _not_ implemented here.

---

## 1. Installation

1. Copy the `electricity_rates.py` script into your project.
2. Make sure you have Python 3 installed.
3. (Optional) Place `green.gif`, `yellow.gif`, and `red.gif` in the same directory if you plan to load icons.

```bash
cp electricity_rates.py /path/to/your/project/
```

---

## 2. Rate Structures

### Seasons
- **Winter**: November 1 → April 30
- **Summer**: May 1 → October 31

### A) Time‑Of‑Use (TOU)

| Tier      | Winter Window                                  | Rate    | Summer Window                                 | Rate    |
|-----------|-------------------------------------------------|---------|-----------------------------------------------|---------|
| Off‑peak  | Weekdays 7 p.m.–7 a.m. + all day weekends/holidays | 7.6 ¢/kWh | Weekdays 7 p.m.–7 a.m. + all day weekends/holidays | 7.4 ¢/kWh |
| Mid‑peak  | Weekdays 11 a.m.–5 p.m.                          | 12.2 ¢/kWh | Weekdays 7 a.m.–11 a.m. & 5 p.m.–7 p.m.           | 10.2 ¢/kWh |
| On‑peak   | Weekdays 7 a.m.–11 a.m. & 5 p.m.–7 p.m.         | 15.8 ¢/kWh | Weekdays 11 a.m.–5 p.m.                         | 15.1 ¢/kWh |

### B) Ultra‑Low Overnight (ULO)

| Tier                 | Window                           | Rate      |
|----------------------|----------------------------------|-----------|
| Ultra‑Low Overnight  | Every day 11 p.m.–7 a.m.         | 2.8 ¢/kWh |
| Weekend Off‑peak     | Weekends & holidays 7 a.m.–11 p.m.| 7.6 ¢/kWh |
| Mid‑peak             | Weekdays 7 a.m.–4 p.m. & 9 p.m.–11 p.m.| 12.2 ¢/kWh |
| On‑peak              | Weekdays 4 p.m.–9 p.m.           | 28.4 ¢/kWh |

---

## 3. Primary Functions

```python
from datetime import datetime, date
from electricity_rates import (
    electricity_rate,
    color_rate,
    rate_level_box,
    load_rate_icon,
)

# (Optional) define holiday dates
holidays = {
    date(2025, 1, 1),    # New Year's Day
    date(2025, 12, 25),  # Christmas
}
```

### 3.1 `electricity_rate(dt=None, holidays=None, schedule='TOU')`
Returns the raw rate (float, $/kWh) for a given datetime and schedule.  
- If `dt` is omitted, uses the current date/time.  
- `schedule` must be `'TOU'` or `'ULO'`.

```py
# Example: TOU rate, Jan 16 2026 at 2 PM
rate = electricity_rate(
    dt=datetime(2026, 1, 16, 14, 0),
    holidays=holidays,
    schedule='TOU',
)
print(rate)       # 0.158 (15.8¢)
```

### 3.2 `color_rate(rate, schedule='TOU')`
Wraps a raw rate in ANSI‑colored text for terminal output.  
- For **TOU**, outputs green/yellow/red based on off‑peak/mid‑peak/on‑peak.  
- For **ULO**, outputs **green** (good) for ultra‑low & weekend off‑peak, **red** (bad) otherwise.

```py
print(color_rate(rate, 'TOU'))  # e.g. "\033[31m$0.158\033[0m"
```

### 3.3 `rate_level_box(dt=None, holidays=None, schedule='TOU')`
Returns a single colored (`■`) box matching the rate level.  

```py
print(rate_level_box(datetime.now(), None, 'ULO'))
# ■ (green or red box)
```

### 3.4 `load_rate_icon(dt=None, holidays=None, schedule='TOU')`
Returns the filename (`.gif`) for a graphical indicator.  

```py
icon_file = load_rate_icon(
    dt=datetime(2026, 1, 16, 14, 0),
    holidays=holidays,
    schedule='ULO',
)
# icon_file == 'red.gif'
```

---

## 4. Putting It All Together

```bash
# To see a full dump of all tests:
python electricity_rates.py
```

This prints each sample datetime with its:  
- Raw colored rate  
- Colored box  
- Gif filename  

Enjoy optimized scheduling for your laundry or EV‑charging—Toronto Hydro style!  

---

*Last updated: April 2025*

