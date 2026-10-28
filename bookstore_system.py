"""
Project Title: Bookstore Inventory and Analytics System
File Name: bookstore_system.py
Description: A complete Python system incorporating Control Structures, Arrays, 
             OOP, NumPy, Pandas, Matplotlib, and Seaborn for managing inventory, 
             analyzing sales, and visualizing trends.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Seaborn visuals styling
sns.set_theme(style="whitegrid")


# ==========================================
# 1. DATASET SETUP & INITIALIZATION
# ==========================================
def initialize_datasets():
    """Sample CSV files create karta hai agar system me na milein."""
    # 1. inventory.csv setup
    if not os.path.exists('inventory.csv'):
        inventory_data = {
            'Title': ['Atomic Habits', 'The Alchemist', 'Python Crash Course', 'Clean Code', 'Deep Work', 'Psychology of Money'],
            'Author': ['James Clear', 'Paulo Coelho', 'Eric Matthes', 'Robert C. Martin', 'Cal Newport', 'Morgan Housel'],
            'Genre': ['Self-Help', 'Fiction', 'Programming', 'Programming', 'Productivity', 'Finance'],
            'Price': [550.0, 320.0, 850.0, 950.0, 480.0, 400.0],
            'Quantity': [25, 40, 15, 10, 30, 50]
        }
        pd.DataFrame(inventory_data).to_csv('inventory.csv', index=False)
        print("[Setup] 'inventory.csv' successfully generate ho gayi.")

    # 2. sales.csv setup
    if not os.path.exists('sales.csv'):
        sales_data = {
            'Date': ['2026-01-15', '2026-01-20', '2026-02-10', '2026-02-22', '2026-03-05', '2026-03-18', '2026-03-25'],
            'Title': ['Atomic Habits', 'Python Crash Course', 'The Alchemist', 'Atomic Habits', 'Clean Code', 'Psychology of Money', 'Deep Work'],
            'Quantity Sold': [5, 3, 10, 4, 2, 8, 6],
            'Total Revenue': [2750.0, 2550.0, 3200.0, 2200.0, 1900.0, 3200.0, 2880.0]
        }
        pd.DataFrame(sales_data).to_csv('sales.csv', index=False)
        print("[Setup] 'sales.csv' successfully generate ho gayi.")


# ==========================================
# 2. BOOKSTORE CLASS (OOP IMPLEMENTATION)
# ==========================================
class Bookstore:
    def __init__(self, inventory_file='inventory.csv', sales_file='sales.csv'):
        self.inventory_file = inventory_file
        self.sales_file = sales_file
        self.load_data()

    def load_data(self):
        """Pandas ke dwara datasets ko read aur clean karna."""
        # Inventory load
        if os.path.exists(self.inventory_file):
            self.inventory_df = pd.read_csv(self.inventory_file)
            self.inventory_df.dropna(inplace=True)
            self.inventory_df['Price'] = self.inventory_df['Price'].astype(float)
            self.inventory_df['Quantity'] = self.inventory_df['Quantity'].astype(int)
        else:
            self.inventory_df = pd.DataFrame(columns=['Title', 'Author', 'Genre', 'Price', 'Quantity'])

        # Sales load
        if os.path.exists(self.sales_file):
            self.sales_df = pd.read_csv(self.sales_file)
            self.sales_df.dropna(inplace=True)
            self.sales_df['Date'] = pd.to_datetime(self.sales_df['Date'], format='mixed')
            self.sales_df['Quantity Sold'] = self.sales_df['Quantity Sold'].astype(int)
            self.sales_df['Total Revenue'] = self.sales_df['Total Revenue'].astype(float)
        else:
            self.sales_df = pd.DataFrame(columns=['Date', 'Title', 'Quantity Sold', 'Total Revenue'])

    def save_data(self):
        """Updated dataframes ko CSV files me save karna."""
        self.inventory_df.to_csv(self.inventory_file, index=False)
        self.sales_df.to_csv(self.sales_file, index=False)

    def add_book(self, title, author, genre, price, quantity):
        """Nayi book add karna (input validation aur control structures ke sath)."""
        if price <= 0:
            print("\n[Error] Book ki Price positive (greater than 0) honi chahiye!")
            return
        if quantity <= 0:
            print("\n[Error] Book ki Quantity positive (greater than 0) honi chahiye!")
            return

        match = self.inventory_df.index[self.inventory_df['Title'].str.lower() == title.lower()].tolist()
        if match:
            idx = match[0]
            self.inventory_df.loc[idx, 'Quantity'] += quantity
            self.inventory_df.loc[idx, 'Price'] = price
            print(f"\n[Success] '{title}' pehle se thi. Stock update karke {self.inventory_df.loc[idx, 'Quantity']} units kiya gaya.")
        else:
            new_row = pd.DataFrame([{
                'Title': title.strip(),
                'Author': author.strip(),
                'Genre': genre.strip(),
                'Price': float(price),
                'Quantity': int(quantity)
            }])
            self.inventory_df = pd.concat([self.inventory_df, new_row], ignore_index=True)
            print(f"\n[Success] Nayi book '{title}' inventory me add kar di gayi!")

        self.save_data()

    def update_inventory(self, title, quantity):
        """Kisi existing book ka stock quantity manually update karna."""
        if quantity < 0:
            print("\n[Error] Quantity negative nahi ho sakti!")
            return

        match = self.inventory_df.index[self.inventory_df['Title'].str.lower() == title.lower()].tolist()
        if match:
            idx = match[0]
            self.inventory_df.loc[idx, 'Quantity'] = int(quantity)
            self.save_data()
            print(f"\n[Success] '{title}' ka total stock ab {quantity} units kar diya gaya hai.")
        else:
            print(f"\n[Error] Book '{title}' inventory me nahi mili.")

    def record_sale(self, title, quantity_sold):
        """Sale record karna, stock deduct karna aur sales file update karna."""
        if quantity_sold <= 0:
            print("\n[Error] Sold quantity 0 se badi honi chahiye!")
            return

        match = self.inventory_df.index[self.inventory_df['Title'].str.lower() == title.lower()].tolist()
        if not match:
            print(f"\n[Error] Book '{title}' inventory me uplabdh nahi hai!")
            return

        idx = match[0]
        current_stock = int(self.inventory_df.loc[idx, 'Quantity'])
        price = float(self.inventory_df.loc[idx, 'Price'])

        if current_stock < quantity_sold:
            print(f"\n[Error] Stock kam hai! Keval {current_stock} units available hain.")
            return

        # Deduct from inventory
        self.inventory_df.loc[idx, 'Quantity'] -= quantity_sold
        total_rev = price * quantity_sold

        # Add to sales
        sale_entry = pd.DataFrame([{
            'Date': pd.Timestamp.now().strftime('%Y-%m-%d'),
            'Title': self.inventory_df.loc[idx, 'Title'],
            'Quantity Sold': int(quantity_sold),
            'Total Revenue': float(total_rev)
        }])
        self.sales_df = pd.concat([self.sales_df, sale_entry], ignore_index=True)
        self.save_data()
        print(f"\n[Success] Sale Recorded: {quantity_sold} x '{title}' | Total Bill: ₹{total_rev:,.2f}")

    def generate_report(self):
        """NumPy aur Pandas use karke overall inventory aur sales summarize karna."""
        print("\n" + "="*50)
        print("          BOOKSTORE SUMMARY REPORT          ")
        print("="*50)

        # NumPy arrays numerical analysis ke liye
        rev_arr = self.sales_df['Total Revenue'].to_numpy()
        prices_arr = self.inventory_df['Price'].to_numpy()
        sales_qty_arr = self.sales_df['Quantity Sold'].to_numpy()

        total_rev = np.sum(rev_arr) if len(rev_arr) > 0 else 0.0
        avg_price = np.mean(prices_arr) if len(prices_arr) > 0 else 0.0
        total_units_sold = np.sum(sales_qty_arr) if len(sales_qty_arr) > 0 else 0

        print(f"Total Revenue Generated : ₹{total_rev:,.2f}")
        print(f"Total Books Sold        : {total_units_sold}")
        print(f"Average Book Price      : ₹{avg_price:,.2f}")
        print(f"Total Distinct Titles   : {len(self.inventory_df)}")
        print(f"Total Stock Available   : {int(np.sum(self.inventory_df['Quantity'].to_numpy())) if len(self.inventory_df) > 0 else 0}")

        # Top-selling analysis using Pandas
        if not self.sales_df.empty:
            grouped_sales = self.sales_df.groupby('Title')['Quantity Sold'].sum()
            top_book = grouped_sales.idxmax()
            top_qty = grouped_sales.max()
            print(f"Best-Selling Book       : {top_book} ({top_qty} copies)")

        print("="*50)

    def visualize_all(self):
        """Matplotlib & Seaborn se 4 visual charts render karna."""
        if self.sales_df.empty or self.inventory_df.empty:
            print("\n[Notice] Visual charts banane ke liye paryapt data nahi hai.")
            return

        # Merging datasets for detailed multi-variable analysis
        merged = pd.merge(self.sales_df, self.inventory_df[['Title', 'Genre', 'Price']], on='Title', how='left')
        merged['Date'] = pd.to_datetime(merged['Date'])
        merged['Month'] = merged['Date'].dt.strftime('%Y-%m')

        fig, axes = plt.subplots(2, 2, figsize=(15, 11))
        plt.subplots_adjust(hspace=0.45, wspace=0.3)

        # 1. Bar Chart: Total sales by Genre
        genre_sales = merged.groupby('Genre')['Quantity Sold'].sum().reset_index()
        sns.barplot(data=genre_sales, x='Genre', y='Quantity Sold', ax=axes[0, 0], palette='Blues_d')
        axes[0, 0].set_title('1. Total Sales by Genre (Bar Chart)', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Copies Sold')
        axes[0, 0].tick_params(axis='x', rotation=20)

        # 2. Line Graph: Monthly Sales Trends
        monthly_sales = merged.groupby('Month')['Total Revenue'].sum().reset_index()
        sns.lineplot(data=monthly_sales, x='Month', y='Total Revenue', marker='o', ax=axes[0, 1], color='#e63946', linewidth=2.5)
        axes[0, 1].set_title('2. Monthly Sales Trends (Line Graph)', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Total Revenue (₹)')

        # 3. Pie Chart: Revenue Share by Book Genre
        genre_rev = merged.groupby('Genre')['Total Revenue'].sum()
        axes[1, 0].pie(genre_rev, labels=genre_rev.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        axes[1, 0].set_title('3. Revenue Share by Genre (Pie Chart)', fontsize=12, fontweight='bold')

        # 4. Heatmap: Correlation between Book Prices and Sales Volumes
        corr_subset = merged[['Price', 'Quantity Sold', 'Total Revenue']].dropna()
        sns.heatmap(corr_subset.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=axes[1, 1], cbar=True)
        axes[1, 1].set_title('4. Correlation: Price vs Sales Volume (Heatmap)', fontsize=12, fontweight='bold')

        plt.suptitle('Bookstore Inventory and Analytics Dashboard', fontsize=16, fontweight='bold')
        plt.show()


# ==========================================
# 3. INTERACTIVE CLI MENU
# ==========================================
def main():
    initialize_datasets()
    store = Bookstore()

    while True:
        print("\n" + "="*35)
        print("  BOOKSTORE MANAGEMENT SYSTEM")
        print("="*35)
        print("1. Add New Book")
        print("2. Update Existing Book Stock")
        print("3. Record a Sale")
        print("4. View Current Inventory Table")
        print("5. Generate Summary Report")
        print("6. Show Data Visualizations")
        print("7. Exit")
        print("="*35)

        choice = input("Enter choice (1-7): ").strip()

        if choice == '1':
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author Name: ").strip()
            genre = input("Enter Genre: ").strip()
            try:
                price = float(input("Enter Price (₹): "))
                quantity = int(input("Enter Quantity: "))
                store.add_book(title, author, genre, price, quantity)
            except ValueError:
                print("\n[Error] Invalid input! Price number honi chahiye aur Quantity integer.")

        elif choice == '2':
            title = input("Enter Book Title to update: ").strip()
            try:
                quantity = int(input("Enter New Stock Quantity: "))
                store.update_inventory(title, quantity)
            except ValueError:
                print("\n[Error] Invalid input! Quantity integer honi chahiye.")

        elif choice == '3':
            title = input("Enter Sold Book Title: ").strip()
            try:
                quantity = int(input("Enter Quantity Sold: "))
                store.record_sale(title, quantity)
            except ValueError:
                print("\n[Error] Invalid input! Quantity integer honi chahiye.")

        elif choice == '4':
            print("\n--- CURRENT INVENTORY TABLE ---")
            if store.inventory_df.empty:
                print("Inventory empty hai.")
            else:
                print(store.inventory_df.to_string(index=False))

        elif choice == '5':
            store.generate_report()

        elif choice == '6':
            print("\nDashboard load ho raha hai...")
            store.visualize_all()

        elif choice == '7':
            print("\nSystem closed. Good day!")
            break
        else:
            print("\n[Error] Galat option chuna hai. Kripya 1 se 7 ke beech enter karein.")


if __name__ == '__main__':
    main()