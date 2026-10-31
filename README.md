# Bookstore Inventory and Analytics System

A menu-driven Python application for running a small bookstore. It keeps track of the **book inventory**, records **sales** (and deducts stock automatically), prints a **summary report**, and renders a four-chart **analytics dashboard**. All data is stored in two plain CSV files, so there is no database to set up.

The project is a practical demonstration of core Python skills: control structures, object-oriented programming, NumPy arrays, Pandas DataFrames, and Matplotlib / Seaborn visualization, all in one script.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Requirements and Installation](#requirements-and-installation)
4. [Quick Start](#quick-start)
5. [Using the Menu](#using-the-menu)
6. [Data Files and Schema](#data-files-and-schema)
7. [How the Code Works](#how-the-code-works)
8. [The Analytics Dashboard](#the-analytics-dashboard)
9. [Summary Report](#summary-report)
10. [Validation and Error Handling](#validation-and-error-handling)
11. [Example Session](#example-session)
12. [Known Limitations and Quirks](#known-limitations-and-quirks)
13. [Troubleshooting](#troubleshooting)
14. [Possible Improvements](#possible-improvements)
15. [License](#license)

---

## Features

- **Inventory management**: add new books, top up stock for existing titles, or set an exact stock level.
- **Sales recording**: records a sale with today's date, calculates the bill from the book's price, and reduces stock. Refuses a sale if there is not enough stock.
- **Persistent storage**: every change is saved immediately to `inventory.csv` and `sales.csv`.
- **Summary report**: total revenue, units sold, average price, number of titles, total stock, and the best-selling book.
- **Analytics dashboard**: bar chart, line graph, pie chart and correlation heatmap in a single 2 x 2 figure.
- **Case-insensitive title matching**: `atomic habits` and `Atomic Habits` refer to the same book.
- **Self-bootstrapping**: if the CSV files are missing, sample data is generated on start-up.
- **Input validation**: rejects non-positive prices and quantities, negative stock, unknown titles and non-numeric input.

---

## Project Structure

```
Bookstore_Inventory_and_Analytics_System/
├── bookstore_system.py   # Entire application (single script, ~300 lines)
├── inventory.csv         # Book catalogue and current stock levels
├── sales.csv             # Log of every sale
└── README.md             # This file
```

---

## Requirements and Installation

**Python:** 3.9 or newer. **Pandas 2.0 or newer is required**, because the code reads dates with `format='mixed'`.

The script was run successfully with: pandas 3.0.5, NumPy 2.5.3, Matplotlib 3.11.2, Seaborn 0.13.2.

| Library      | Purpose                                              |
|--------------|------------------------------------------------------|
| `pandas`     | Loading, cleaning, merging and grouping the data     |
| `numpy`      | Fast numeric aggregates in the summary report        |
| `matplotlib` | Figure layout, pie chart, displaying the dashboard   |
| `seaborn`    | Theme, bar chart, line plot, heatmap                 |

The standard-library modules `os` and `datetime` are also imported (no installation needed).

```bash
# 1. Clone the repository
git clone https://github.com/korichirag-arch/Bookstore_Inventory_and_Analytics_System.git
cd Bookstore_Inventory_and_Analytics_System

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install numpy pandas matplotlib seaborn
```

The repository has no `requirements.txt`; the four package names above are all you need.

---

## Quick Start

```bash
python bookstore_system.py
```

> **Run it from inside the project folder.** The CSV files are opened by relative name (`inventory.csv`, `sales.csv`), so they are looked up in whatever folder you launch Python from. Launching from elsewhere will create a fresh set of sample files there.

You will see the main menu. Type a number from 1 to 7 and press Enter.

---

## Using the Menu

```
===================================
  BOOKSTORE MANAGEMENT SYSTEM
===================================
1. Add New Book
2. Update Existing Book Stock
3. Record a Sale
4. View Current Inventory Table
5. Generate Summary Report
6. Show Data Visualizations
7. Exit
===================================
```

| Option | What it asks for | What it does |
|--------|------------------|--------------|
| **1. Add New Book** | Title, Author, Genre, Price (₹), Quantity | If the title is new, adds a row. If the title already exists, **adds the quantity to existing stock and overwrites the price** (author and genre you type are ignored). |
| **2. Update Existing Book Stock** | Title, New Stock Quantity | Sets the stock to exactly that number (it is **not** added to the current stock). `0` is allowed. |
| **3. Record a Sale** | Title, Quantity Sold | Checks stock, deducts the quantity, computes `price x quantity`, and appends a row to the sales log dated today. |
| **4. View Current Inventory Table** | none | Prints the inventory as a table. |
| **5. Generate Summary Report** | none | Prints the report described [below](#summary-report). |
| **6. Show Data Visualizations** | none | Opens the 4-chart dashboard. Close the window to return to the menu. |
| **7. Exit** | none | Quits the program. |

Any other input prints an error and shows the menu again.

---

## Data Files and Schema

### `inventory.csv`

| Column     | Type    | Meaning                         |
|------------|---------|---------------------------------|
| `Title`    | text    | Book title (used as the unique key) |
| `Author`   | text    | Author name                     |
| `Genre`    | text    | Genre label                     |
| `Price`    | float   | Unit price in rupees (₹)        |
| `Quantity` | integer | Units currently in stock        |

### `sales.csv`

| Column          | Type     | Meaning                                       |
|-----------------|----------|-----------------------------------------------|
| `Date`          | datetime | Date of the sale                              |
| `Title`         | text     | Title sold (must match an inventory title)    |
| `Quantity Sold` | integer  | Number of copies in this sale                 |
| `Total Revenue` | float    | Bill amount, `price x quantity` at time of sale |

### Data included in the repository

The repository ships with 8 titles in inventory and 8 sale records:

| Title               | Author           | Genre        | Price (₹) | Stock |
|---------------------|------------------|--------------|-----------|-------|
| Atomic Habits       | James Clear      | Self-Help    | 550       | 25    |
| The Alchemist       | Paulo Coelho     | Fiction      | 320       | 40    |
| Python Crash Course | Eric Matthes     | Programming  | 850       | 15    |
| Clean Code          | Robert C. Martin | Programming  | 950       | 10    |
| Deep Work           | Cal Newport      | Productivity | 480       | 30    |
| Psychology of Money | Morgan Housel    | Finance      | 400       | 50    |
| Bleach              | Chirga           | `45`         | 450       | 525   |
| AOT                 | CHiku            | `65`         | 500       | 55    |

The first six books are the built-in sample data. The last two (Bleach, AOT) were added through the menu, and they have numeric genres (`45`, `65`). That looks like a number was typed into the Genre prompt by mistake; see [Known Limitations](#known-limitations-and-quirks).

### Automatic sample data

`initialize_datasets()` creates `inventory.csv` (6 books) and `sales.csv` (7 sales from January to March 2026) **only if the files do not exist**. Existing files are never overwritten by this step.

### Date format

The very first sales are written as plain dates (`2026-01-15`). After the program saves, Pandas writes them with a time part (`2026-01-15 00:00:00`), while new sales are recorded as plain dates. The loader handles both with `pd.to_datetime(..., format='mixed')`.

---

## How the Code Works

### Program flow

```
 start
   │
   ▼
 initialize_datasets()   ── create sample CSVs if missing
   │
   ▼
 Bookstore()             ── load_data(): read CSVs, drop incomplete rows, fix types
   │
   ▼
 ┌─► show menu ──► read choice ──► call matching Bookstore method
 │                                      │
 │                       (add / update / sale → save_data() writes both CSVs)
 └──────────────────────────────────────┘        choice 7 ──► exit
```

### Module layout (`bookstore_system.py`)

| Lines | Part | Role |
|-------|------|------|
| 9 to 17 | Imports and theme | Loads libraries and sets the Seaborn `whitegrid` theme |
| 23 to 46 | `initialize_datasets()` | Creates the sample CSVs when absent |
| 52 to 229 | `class Bookstore` | All business logic and analytics |
| 235 to 299 | `main()` | The interactive menu loop |
| 302 to 303 | `if __name__ == '__main__'` | Entry point; importing the file does not start the menu |

### The `Bookstore` class

| Method | What it does |
|--------|--------------|
| `__init__(inventory_file='inventory.csv', sales_file='sales.csv')` | Stores the file names and calls `load_data()`. Different file names can be passed in. |
| `load_data()` | Reads both CSVs into `inventory_df` and `sales_df`, drops any row with a missing value, converts `Price` and `Total Revenue` to float, `Quantity` and `Quantity Sold` to int, and parses `Date`. If a file is missing, it uses an empty DataFrame with the correct columns. |
| `save_data()` | Writes both DataFrames back to their CSV files. |
| `add_book(title, author, genre, price, quantity)` | Validates `price > 0` and `quantity > 0`. Finds the title case-insensitively; adds stock if found, otherwise appends a new row. Saves. |
| `update_inventory(title, quantity)` | Rejects negative values and unknown titles; otherwise sets the stock exactly and saves. |
| `record_sale(title, quantity_sold)` | Rejects non-positive quantities and unknown titles; rejects the sale if stock is too low; otherwise deducts stock, computes revenue from the current price, appends a sales row dated today, saves. |
| `generate_report()` | Converts columns to NumPy arrays and prints totals, then uses a Pandas `groupby` to find the best seller. |
| `visualize_all()` | Merges sales with inventory and draws the four-chart dashboard. |

### Libraries used for each job

- **Pandas**: reading and writing CSV, cleaning, row lookup by title, `concat`, `merge`, `groupby`.
- **NumPy**: `to_numpy()`, `np.sum`, `np.mean` for the report figures.
- **Matplotlib**: the 2 x 2 subplot grid, the pie chart, `plt.show()`.
- **Seaborn**: `barplot`, `lineplot`, `heatmap`, colour palettes and theme.

---

## The Analytics Dashboard

Menu option 6 first joins each sale to its book's `Genre` and `Price` (a left join on `Title`) and extracts the sale month. It then draws four charts in a 15 x 11 inch figure titled *Bookstore Inventory and Analytics Dashboard*:

| # | Chart | Question it answers |
|---|-------|---------------------|
| 1 | **Bar chart**: copies sold per genre | Which genres sell the most units? |
| 2 | **Line graph**: total revenue per month (red line with markers) | How is revenue trending over time? |
| 3 | **Pie chart**: revenue share per genre (with percentages) | Which genres bring in the most money? |
| 4 | **Heatmap**: correlation of `Price`, `Quantity Sold`, `Total Revenue` | Do pricier books sell fewer copies? |

If either table is empty, the dashboard is skipped and a notice is printed.

How to read chart 4: values run from -1 to +1. With the included data, price and units sold have a correlation of about **-0.89** (pricier books sold fewer copies). Keep in mind that this is computed from only a handful of sales, and `Total Revenue` is derived from price and quantity, so its correlations are partly mechanical.

---

## Summary Report

Menu option 5 prints:

```
==================================================
          BOOKSTORE SUMMARY REPORT
==================================================
Total Revenue Generated : ₹21,180.00
Total Books Sold        : 43
Average Book Price      : ₹562.50
Total Distinct Titles   : 8
Total Stock Available   : 750
Best-Selling Book       : The Alchemist (10 copies)
==================================================
```

These are the actual values produced from the data currently in the repository. The figures change as you add books and record sales.

| Line | How it is computed |
|------|--------------------|
| Total Revenue Generated | Sum of `Total Revenue` over all sales |
| Total Books Sold | Sum of `Quantity Sold` over all sales |
| Average Book Price | Mean of `Price` across inventory titles (a simple average over titles, not weighted by stock or sales) |
| Total Distinct Titles | Number of rows in inventory |
| Total Stock Available | Sum of `Quantity` across inventory |
| Best-Selling Book | Title with the largest total `Quantity Sold`, summed across all its sales |

With empty data, the report prints zeros instead of crashing.

---

## Validation and Error Handling

| Situation | Behaviour |
|-----------|-----------|
| Price or quantity is zero or negative when adding a book | Error message; nothing changes |
| Non-numeric price or quantity typed in the menu | Caught (`ValueError`); error message; back to the menu |
| New stock level is negative | Error message; nothing changes |
| Title not found (update or sale) | Error message; nothing changes |
| Sale quantity is zero or negative | Error message; nothing changes |
| Sale quantity exceeds stock | Error message showing the available units; no sale is recorded |
| Invalid menu choice | Error message; menu is shown again |
| CSV file missing at load time | Empty tables are used; reports show zeros |
| Rows with missing values in a CSV | Silently dropped on load |

Messages are written in a Hindi-English (Hinglish) mix, for example `Stock kam hai!` means "Stock is low!".

---

## Example Session

```text
Enter choice (1-7): 3
Enter Sold Book Title: atomic habits
Enter Quantity Sold: 2

[Success] Sale Recorded: 2 x 'atomic habits' | Total Bill: ₹1,100.00

Enter choice (1-7): 3
Enter Sold Book Title: Clean Code
Enter Quantity Sold: 11

[Error] Stock kam hai! Keval 10 units available hain.

Enter choice (1-7): 1
Enter Book Title: Deep Work
Enter Author Name: x
Enter Genre: y
Enter Price (₹): 500
Enter Quantity: 5

[Success] 'Deep Work' pehle se thi. Stock update karke 35 units kiya gaya.
```

Notice in the last example that the title already existed, so the stock grew (30 to 35), the price was changed to 500, and the author and genre were ignored.

---

## Known Limitations and Quirks

These behaviours were confirmed by running the code. They are not crashes, but they are worth knowing about.

1. **Adding an existing title overwrites its price.** Quantity is added, the price is replaced with the new value, and author/genre are ignored.
2. **Historical revenue uses the price at the moment of sale.** If you later change a price, old sales are not recalculated (which is usually the correct behaviour), but the `Price` used in the dashboard's correlation heatmap is the *current* price.
3. **Genre is free text with no validation.** A number such as `45` or `65` is accepted and shows up as its own genre in the bar and pie charts. This already happens in the shipped data: genre `65` (AOT) appears in both charts, and `45` (Bleach) will appear as soon as that book sells.
4. **Title is the only key.** There are no book IDs or ISBNs. If two inventory rows ever shared a title, the dashboard's join would count their sales twice.
5. **Monthly line chart uses months as text labels.** Months with no sales (for example April to September in the sample data) do not appear as gaps; the line connects the months that exist.
6. **Seaborn deprecation warning.** With Seaborn 0.13 the bar chart prints a `FutureWarning` about `palette` without `hue`. It still works, but the call needs a small change before Seaborn 0.14.
7. **Relative file paths.** Data files are read from the current working directory, not from the script's folder.
8. **Charts block the menu.** `plt.show()` waits for you to close the window. On a machine without a display, set `MPLBACKEND=Agg` (nothing will be shown).
9. **Whole files are rewritten on every change**, and there is no locking, so do not run two copies of the program at the same time on the same files.
10. **Unused import.** `from datetime import datetime` is never used (`pd.Timestamp.now()` is used instead).
11. **No delete, search or low-stock features**, no sales history per customer, and no undo.
12. **Empty text is accepted.** Blank titles, authors and genres are not rejected when adding a book.

---

## Troubleshooting

| Problem | Likely cause and fix |
|---------|----------------------|
| `ModuleNotFoundError: No module named 'seaborn'` (or `pandas`, `numpy`, `matplotlib`) | Run `pip install numpy pandas matplotlib seaborn`. |
| `ValueError` mentioning `format='mixed'` | Your pandas is older than 2.0. Run `pip install --upgrade pandas`. |
| The program shows only 6 books and 7 sales | You launched it from a different folder, so it generated new sample files there. `cd` into the project folder and run it again. |
| The menu does not come back after choosing 6 | A chart window is open, possibly behind other windows. Close it. |
| No chart window on a server | There is no display. Use `MPLBACKEND=Agg python bookstore_system.py`, or add `plt.savefig("dashboard.png")` before `plt.show()`. |
| `[Notice] Visual charts banane ke liye paryapt data nahi hai.` | Either the inventory or the sales table is empty. Record at least one sale first. |
| A book "disappeared" after editing a CSV by hand | A row with an empty cell is dropped when the file is loaded. Fill in every column. |
| A sale is refused for a book that exists | Check the spelling (case does not matter, but extra characters do) and that the stock is large enough. |

---

## Possible Improvements

- Add a unique book ID or ISBN and use it instead of the title as the key.
- Validate genre (text only, or choose from a list) and reject blank fields.
- Make `add_book` for an existing title ask before changing the price.
- Resolve the paths relative to the script file, not the working directory.
- Fix the Seaborn `palette` / `hue` warning in the bar chart.
- Plot revenue on a real date axis so months without sales show as gaps.
- Add features: low-stock alerts, delete a book, search, sales for a date range, top *N* books, export report to a file.
- Save the dashboard as an image and add a `requirements.txt`.
- Add automated tests for `add_book`, `update_inventory` and `record_sale`.
- Move storage to SQLite if more than one user or larger data is needed.

---

## License

No license file is included in this repository yet. Add one (for example MIT) if you want others to reuse the code.
