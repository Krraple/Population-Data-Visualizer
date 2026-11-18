# Population Data Visualizer

## Project Overview

The **Population Data Visualizer (PS No. 26)** is a Python project that reads city population records from a CSV file, calculates population statistics, and displays the results using charts. It also allows users to enter new city population data through a menu-driven interface.

The project uses dummy population data for demonstration and analysis.

## Objectives

- Read population data containing a city, year, and population.
- Calculate the latest total population across the cities.
- Identify the city with the largest latest population.
- Calculate each city's population growth percentage when data from at least two different years is available.
- Display population growth and population trends through charts.
- Allow users to add and save new population records.

## Technologies and Libraries

- **Python** – main programming language.
- **Pandas** – reading, cleaning, organizing, and analysing CSV data.
- **Matplotlib** – creating the bar chart and line chart.

Install the required libraries with:

```bash
pip install -r requirements.txt
```

## Input Data

The CSV file uses three fields:

```text
City,Year,Population
```

Each record represents the population of a city in a particular year. The program can read a CSV file without a header row and also skips a header row if one is present.

## Main Features

### 1. Data validation

The `check_row()` function checks each record before it is accepted:

- City name must not be empty.
- Year must be a whole number.
- Population must be a valid number greater than zero.
- City names are cleaned and formatted consistently.

Invalid records are skipped with an error message. Duplicate records for the same city and year are removed when the CSV is loaded.

### 2. CSV loading and saving

The `load_data()` function reads the CSV file using Pandas and prepares the valid records for analysis. If the file is missing or empty, the program starts with an empty dataset.

The `save_data()` function saves the updated data back to the CSV file without adding a header row.

### 3. Population statistics

The `get_stats()` function groups records by city and finds the earliest and latest years and their corresponding populations.

The population growth formula is:

\[
\text{Growth (\%)} =
\frac{\text{Latest Population} - \text{Earliest Population}}
{\text{Earliest Population}} \times 100
\]

If a city has data for only one year, its growth is shown as unavailable because there is no earlier value for comparison.

The summary also calculates the total of each city's latest recorded population, identifies the largest city, and identifies the fastest-growing city when growth data is available.

### 4. Data visualization

The `draw_charts()` function displays two charts in one Matplotlib window:

- **Population Growth by City (bar chart):** compares the growth percentage of each city. Positive growth is shown in green and negative growth in red.
- **Population Trend (line chart):** shows each city's recorded population across the available years.

The charts are saved as `charts.png`. They are refreshed when new data is added.

### 5. Menu-driven interface

When the program runs, it displays these options:

1. **Summary** – displays the population summary.
2. **Growth and charts** – displays growth percentages and opens both charts.
3. **Add new data** – accepts a city, year, and population, validates the entry, saves it, and refreshes the summary and charts.
4. **View all data** – displays all currently loaded records.
5. **Exit** – closes the program.

## How to Run

1. Make sure Python is installed.
2. Open a terminal in the project folder.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the program:

   ```bash
   python population_visualizer.py
   ```

To use a different CSV file, provide its path as an argument:

```bash
python population_visualizer.py some_other_file.csv
```

## Sample Output

The supplied chart illustrates the following growth calculations:

| City | Earlier population | Latest population | Growth |
|---|---:|---:|---:|
| Raipur | 1,000,000 (2020) | 1,100,000 (2024) | +10.0% |
| Durg | 500,000 (2020) | 600,000 (2024) | +20.0% |

The line chart also plots Raipur and Durg from 2020 to 2024. It includes a separate Raigrah data point for 2025; because the supplied data contains only one year for Raigrah, no growth percentage can be calculated for that city.

## Testing

The project README describes tests for:

- Normal population data.
- A boundary case where a city has only one year's data.
- Invalid population values and non-positive populations.
- Displaying the growth results and charts.

The normal test data gives a combined latest population of **1,700,000**, with **Raipur** as the largest city and **Durg** as the fastest-growing city at **20.00%**.

## Conclusion

The Population Data Visualizer demonstrates how Python, Pandas, and Matplotlib can be used together to validate and analyse CSV data and present the results visually. Its menu-driven design makes it possible to view statistics, inspect records, add new data, and refresh charts without manually editing the program.
