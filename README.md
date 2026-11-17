# Population Data Visualizer (PS No. 26)

**Name:** _your name_  **Roll No.:** _your roll number_

## Problem
Analyse city population data from a CSV file (`City, Year, Population`): find the total
population, the largest city and each city's growth, and show the results with charts.
Growth % = (latest - earliest) / earliest x 100. Only dummy data is used.

## How to run
```
pip install -r requirements.txt
python population_visualizer.py
```
Menu: 1 Summary | 2 Growth and charts | 3 Add new data | 4 View all data | 5 Exit

**Option 3 lets you type your own data.** It is saved in `population.csv`, and the
summary and the charts are refreshed straight away.

## How the program works
1. **check_row()** - checks one row: city not empty, year is a whole number,
   population is a number and above 0.
2. **load_data()** - reads the CSV with Pandas, uses check_row() on every row, skips bad
   rows with a message (`Row 2 skipped: ...`) and removes duplicates.
3. **get_stats()** - uses `groupby("City")` to get each city's first/latest population and
   its growth %. One year of data = no growth.
4. **show_summary()** - total population (sum of each city's latest value), largest city,
   fastest growing city.
5. **draw_charts()** - one window with a bar chart (growth by city) and a line chart
   (population trend). It is called again after every change, so charts always match the data.
6. **add_data()** - asks for City, Year, Population, checks it, saves it to the CSV, then
   shows the new summary and refreshes the charts.

## Test cases (all pass)
| # | File | Option | Output |
|---|---|---|---|
| 1 Normal | test1_normal.csv | 1 | Total population (2024): 1700000, Largest city: Raipur (1100000), Fastest growing: Durg (+20.00%) |
| 2 Boundary | test2_minimum.csv | 1 | Total population: 1100000 \| Largest city: Raipur, Growth: not available (only one year of data) |
| 3 Invalid | test3_invalid.csv | 1 | Row 2 skipped: invalid Population 'abc'. Row 3 skipped: Population must be positive. Valid rows: 1 |
| 4 Charts | test1_normal.csv | 2 | Raipur: +10.00% \| Durg: +20.00%, both charts displayed |

To run a test file: `python population_visualizer.py test3_invalid.csv`
