"""
Population Data Visualizer (PS No. 26) - simple version

You can type in your own city data. Every time the data changes, the
summary and the charts are refreshed.

Run:  python population_visualizer.py
      python population_visualizer.py some_other_file.csv

CSV format (no header needed):  City,Year,Population
Growth % = (latest - earliest) / earliest * 100
"""

import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
FILE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "population.csv")
COLUMNS = ["City", "Year", "Population"]


# ---------------------------------------------------------------
# STEP 1: check one row of data (used for the file AND for typing)
# ---------------------------------------------------------------
def check_row(city, year, pop):
    """Return (row, None) if the data is fine, or (None, error message)."""
    city = "" if pd.isna(city) else str(city).strip().title()
    year = "" if pd.isna(year) else str(year).strip()
    pop = "" if pd.isna(pop) else str(pop).strip()

    if city == "":
        return None, "City is missing."
    if not year.isdigit():
        return None, f"invalid Year '{year}'."
    try:
        pop_number = int(float(pop))
    except (ValueError, OverflowError):
        return None, f"invalid Population '{pop}'."
    if pop_number <= 0:
        return None, "Population must be positive."

    return {"City": city, "Year": int(year), "Population": pop_number}, None


# ---------------------------------------------------------------
# STEP 2: load the CSV with Pandas and clean it
# ---------------------------------------------------------------
def load_data(path):
    if not os.path.isfile(path):
        print("No data file found - starting with empty data.")
        return pd.DataFrame(columns=COLUMNS)
    try:
        raw = pd.read_csv(path, header=None, names=COLUMNS, dtype=str,
                          skipinitialspace=True)
    except pd.errors.EmptyDataError:
        print("The file is empty - starting with empty data.")
        return pd.DataFrame(columns=COLUMNS)

    # skip a header line such as "City,Year,Population"
    if len(raw) > 0 and str(raw.iloc[0]["Year"]).strip().lower() == "year":
        raw = raw.iloc[1:]

    good_rows = []
    for number, (_, r) in enumerate(raw.iterrows(), start=1):
        row, error = check_row(r["City"], r["Year"], r["Population"])
        if error:
            print(f"Row {number} skipped: {error}")
        else:
            good_rows.append(row)

    df = pd.DataFrame(good_rows, columns=COLUMNS)
    df = df.drop_duplicates(subset=["City", "Year"])      # remove duplicates
    print(f"Valid rows: {len(df)}")
    return df


def save_data(df):
    df.to_csv(FILE, header=False, index=False)


# ---------------------------------------------------------------
# STEP 3: the calculation - groupby() gives one result per city
# ---------------------------------------------------------------
def get_stats(df):
    df = df.sort_values("Year", kind="stable")
    stats = df.groupby("City", sort=False).agg(
        first_year=("Year", "first"),
        last_year=("Year", "last"),
        first_pop=("Population", "first"),
        latest=("Population", "last"),
    )
    stats["growth"] = (stats["latest"] - stats["first_pop"]) / stats["first_pop"] * 100
    # a city with only one year of data has no growth
    stats.loc[stats["first_year"] == stats["last_year"], "growth"] = float("nan")
    return stats


# ---------------------------------------------------------------
# STEP 4: menu option 1 - summary
# ---------------------------------------------------------------
def show_summary(df):
    if df.empty:
        print("No data yet. Use option 3 to add some.")
        return
    stats = get_stats(df)
    total = stats["latest"].sum()
    biggest = stats["latest"].idxmax()
    growth = stats["growth"].dropna()

    if growth.empty:
        print(f"Total population: {total} | Largest city: {biggest}")
        print("Growth: not available (only one year of data)")
    else:
        print(f"Total population ({stats['last_year'].max()}): {total}")
        print(f"Largest city: {biggest} ({stats.loc[biggest, 'latest']})")
        fastest = growth.idxmax()
        print(f"Fastest growing: {fastest} ({growth[fastest]:+.2f}%)")


# ---------------------------------------------------------------
# STEP 5: menu option 2 - growth and charts
# ---------------------------------------------------------------
def draw_charts(df):
    """Draw both charts in ONE window. Calling it again redraws the window
    with the new data, so the charts always match the data."""
    stats = get_stats(df)
    growth = stats["growth"].dropna()

    fig = plt.figure("Population Data Visualizer", figsize=(11, 4.5))
    fig.clf()
    bar_ax, line_ax = fig.subplots(1, 2)

    # bar chart: growth % of each city
    if growth.empty:
        bar_ax.text(0.5, 0.5, "Growth not available\n(need 2 different years)",
                    ha="center", va="center", transform=bar_ax.transAxes)
    else:
        colours = ["tab:green" if g >= 0 else "tab:red" for g in growth]
        bars = bar_ax.bar(growth.index, growth.values, color=colours)
        bar_ax.bar_label(bars, fmt="%+.1f%%")
    bar_ax.set_title("Population Growth by City")
    bar_ax.set_xlabel("City")
    bar_ax.set_ylabel("Growth (%)")

    # line chart: population of each city over the years
    for city, part in df.sort_values("Year").groupby("City", sort=False):
        line_ax.plot(part["Year"], part["Population"], marker="o", label=city)
    line_ax.set_title("Population Trend")
    line_ax.set_xlabel("Year")
    line_ax.set_ylabel("Population")
    line_ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    line_ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    line_ax.legend(title="City")
    line_ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "charts.png"), dpi=110)
    plt.pause(0.1)          # lets the window update without stopping the program


def show_growth_and_charts(df):
    if df.empty:
        print("No data yet. Use option 3 to add some.")
        return
    growth = get_stats(df)["growth"].dropna()
    if growth.empty:
        print("Growth: not available (only one year of data)")
    else:
        print(" | ".join(f"{city}: {g:+.2f}%" for city, g in growth.items()))
    draw_charts(df)
    if growth.empty:
        print("Line chart 'Population Trend' displayed")
    else:
        print("Bar chart 'Population Growth by City' and "
              "line chart 'Population Trend' displayed")


# ---------------------------------------------------------------
# STEP 6: menu option 3 - add your own data
# ---------------------------------------------------------------
def add_data(df):
    city = input("City: ")
    year = input("Year: ")
    pop = input("Population: ")

    row, error = check_row(city, year, pop)
    if error:
        print(f"Not added: {error}")
        return df

    # if this city + year already exists, replace the old number
    same = (df["City"] == row["City"]) & (df["Year"] == row["Year"])
    df = pd.concat([df[~same], pd.DataFrame([row])], ignore_index=True)
    save_data(df)
    print(f"Saved: {row['City']}, {row['Year']}, {row['Population']}")

    # data changed -> show the new summary and refresh the charts
    show_summary(df)
    draw_charts(df)
    return df


# ---------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------
def main():
    plt.ion()                       # keep the chart window open while we type
    df = load_data(FILE)

    while True:
        print("\n===== Population Data Visualizer =====")
        print("1. Summary")
        print("2. Growth and charts")
        print("3. Add new data")
        print("4. View all data")
        print("5. Exit")
        try:
            choice = input("Enter your choice (1-5): ").strip()
        except EOFError:
            break

        if choice == "1":
            show_summary(df)
        elif choice == "2":
            show_growth_and_charts(df)
        elif choice == "3":
            df = add_data(df)
        elif choice == "4":
            print(df.to_string(index=False) if not df.empty else "No data yet.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 to 5.")

    plt.close("all")


if __name__ == "__main__":
    main()
