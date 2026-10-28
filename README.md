# Bookstore Inventory and Analytics System

A comprehensive Python-based system designed to manage bookstore inventory, track and record sales operations, and deliver numerical insights and visual analytics. The project implements Object-Oriented Programming (OOP), Control Structures, NumPy, Pandas, Matplotlib, and Seaborn.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technical Architecture](#technical-architecture)
- [Dataset Specifications](#dataset-specifications)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Usage Instructions](#usage-instructions)
- [Visualizations Included](#visualizations-included)
- [License](#license)

---

## Project Overview

The Bookstore Inventory and Analytics System streamlines daily bookstore workflows:
1. Maintaining catalog records (adding books, updating stock, inventory tracking).
2. Processing customer sales and auto-updating available stocks.
3. Generating automated business summary reports using numerical computing.
4. Providing statistical dashboards and graphical visualizations for sales trends and correlations.

---

## Key Features

- Input Validation: Uses control structures to verify price, stock count, and positive numeric values.
- OOP Design: Encapsulates business logic within the core Bookstore class.
- Dynamic Data Handling: Automatically loads, cleans, updates, and saves CSV files using Pandas.
- High-Performance Computations: Uses NumPy arrays to compute total revenue, averages, and volume aggregations.
- Data Visualizations: Displays genre-wise distributions, revenue trends, and correlation heatmaps.

---

## Technical Architecture

- Language: Python 3.8+
- Data Analysis & Cleaning: Pandas
- Numerical Computations: NumPy
- Data Visualization: Matplotlib, Seaborn
- Storage: Flat CSV files (inventory.csv, sales.csv)

---

## Dataset Specifications

The project operates on two relational CSV data structures:

### 1. inventory.csv
- Title: Name of the book (String)
- Author: Author of the book (String)
- Genre: Book category/genre (String)
- Price: Unit cost in INR (Float)
- Quantity: Available stock level (Integer)

### 2. sales.csv
- Date: Date of transaction (YYYY-MM-DD)
- Title: Title of the book sold (String)
- Quantity Sold: Units purchased (Integer)
- Total Revenue: Total billing amount (Float)

---

## Project Structure

```text
bookstore-inventory-analytics/
│
├── bookstore_system.py   # Main executable script containing OOP class and CLI menu
├── inventory.csv         # Inventory dataset
├── sales.csv             # Transactional sales dataset
└── README.md             # Project documentation and setup guide
[Chirag Kori]
