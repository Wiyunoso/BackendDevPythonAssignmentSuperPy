from rich.table import Column, Table
from rich.align import Align
from rich.console import Console
import datetime
import csv
from sub_functions import (
    get_current_date,
    list_of_rows_and_sum_of_multiplication_from_2_columns_from_specified_CSV_over_specified_period,
)

bought_csv_file = "./csv_files/bought.csv"
sold_csv_file = "./csv_files/sold.csv"
expired_csv_file = "./csv_files/expired.csv"


console = Console()


def report_inventory(report_date=get_current_date("string")):
    inventory_table = Table(
        "Expiration Date",
        "Id",
        "Buy Date",
        "Product Name",
        title="Inventory Report of " + report_date,
        title_style="bold red",
        caption="End of Inventory Report of " + report_date,
        caption_style="bold red",
        style="green",
    )
    inventory_table.add_column("Quantity", justify="right")

    report_date_obj = datetime.datetime.strptime(report_date, "%Y-%m-%d")

    """ This method to get the inventory of a certain date differs from the one where the current date is set (where the inventory, expired and sold file has to be adjusted to the new date).
    With setting a new date in the past, there is also the possibility to sell (and buy) things in the past, and thereby changing the inventory of the past. The already registrated sales counting from that new date on, are therefore not valid anymore, as they were based on an inventory before the change. 
    Id est: when adding a sale in the past, the already registrated sale later may not be possible anymore, because that product may be already out of stock due to that newly added sale in the past.
    Therefore, when setting the current date in the past, the sales registration will be undone till that new date in the past.
    When only asking for an inventory report from the past, where there is no possibiliy to sell, it's not necessary and not desirable to delete sales registration."""

    # The method below is based on:
    # (inventory = bought - sold - expired) from start up til the report_date

    with open(bought_csv_file, "r", newline="") as bought_file:
        bought_list = list(csv.DictReader(bought_file))

    with open(sold_csv_file, "r", newline="") as sold_file:
        sold_list = list(csv.DictReader(sold_file))

    inventory_list = []

    for bought_product in bought_list:
        if (
            datetime.datetime.strptime(bought_product["expiration_date"], "%Y-%m-%d")
            >= report_date_obj
            and datetime.datetime.strptime(bought_product["buy_date"], "%Y-%m-%d")
            <= report_date_obj
        ):
            inventory_list.append(bought_product)

    inventory_list_copy = inventory_list.copy()
    for sold_product in sold_list:
        if (
            datetime.datetime.strptime(sold_product["sales_date"], "%Y-%m-%d")
            <= report_date_obj
        ):
            for inventory_product in inventory_list_copy:
                if sold_product["Id"] == inventory_product["Id"]:
                    inventory_product["quantity"] = int(
                        inventory_product["quantity"]
                    ) - int(sold_product["quantity"])
                    if inventory_product["quantity"] == 0:
                        inventory_list.remove(inventory_product)

    inventory_list.sort(
        key=lambda row: datetime.datetime.strptime(row["expiration_date"], "%Y-%m-%d")
    )
    for inventory_product in inventory_list:
        inventory_table.add_row(
            inventory_product["expiration_date"],
            inventory_product["Id"],
            inventory_product["buy_date"],
            inventory_product["product_name"],
            str(inventory_product["quantity"]),
        )

    console.print(inventory_table)


def report_revenue(date_1, date_2):
    revenue_table = Table(
        "Id",
        "Sales Date",
        "Product Name",
        title="Revenue Report between " + date_1 + " and " + date_2 + ".",
        title_style="bold green",
        style="green",
    )
    revenue_table.add_column("Quantity", justify="right")
    revenue_table.add_column("Sales Price", justify="right")
    revenue_table.add_column("Single Sale Revenue", justify="right")

    revenue, sold_list = get_revenue(date_1, date_2)

    for sold_product in sold_list:
        revenue_table.add_row(
            sold_product["Id"],
            sold_product["sales_date"],
            sold_product["product_name"],
            sold_product["quantity"],
            str(sold_product["sales_price"]),
            str(sold_product["row_multiplication"]),
        )

    console.print(revenue_table)
    console.print(
        f"The revenue between {date_1} and {date_2} is {revenue:.2f} euro",
        style="green",
    )


def get_revenue(date_1, date_2):
    return list_of_rows_and_sum_of_multiplication_from_2_columns_from_specified_CSV_over_specified_period(
        date_1, date_2, "sales_date", sold_csv_file, "quantity", "sales_price"
    )


def report_profit(date_1, date_2):
    report_revenue(date_1, date_2)
    revenue, sold_list = get_revenue(date_1, date_2)
    expenses, bought_list = get_expenses(date_1, date_2)
    profit = revenue - expenses

    expenses_table = Table(
        "Id",
        "Buy Date",
        "Product Name",
        title="Expenses Report between " + date_1 + " and " + date_2 + ".",
        title_style="bold red",
        style="red",
    )
    expenses_table.add_column("Quantity", justify="right")
    expenses_table.add_column("Buy Price", justify="right")
    expenses_table.add_column("Single Buy Expense", justify="right")

    for bough_product in bought_list:
        expenses_table.add_row(
            bough_product["Id"],
            bough_product["buy_date"],
            bough_product["product_name"],
            bough_product["quantity"],
            str(bough_product["buy_price"]),
            str(bough_product["row_multiplication"]),
        )

    console.print(expenses_table)
    console.print(
        f"The expenses between {date_1} and {date_2} is {expenses:.2f} euro.",
        style="red",
    )
    console.print(
        f"The profit between {date_1} and {date_2} is {profit:.2f} euro.",
        style="yellow",
    )


def get_expenses(date_1, date_2):
    return list_of_rows_and_sum_of_multiplication_from_2_columns_from_specified_CSV_over_specified_period(
        date_1, date_2, "buy_date", bought_csv_file, "quantity", "buy_price"
    )

def report_expired_products():
    expired_table = Table(
    "Expiration Date",
    "Id",
    "Buy Date",
    "Product Name",
    title="Expired Report of " + get_current_date('string'),
    title_style="bold red",
    caption="End of Expired Report of " + get_current_date('string'),
    caption_style="bold red",
    style="green",
    )
    expired_table.add_column("Quantity", justify="right")

    with open(expired_csv_file, "r", newline="") as file:
        expired_products_list = list(csv.DictReader(file))

        for expired_product in expired_products_list:
            expired_table.add_row(
            expired_product["expiration_date"],
            expired_product["Id"],
            expired_product["buy_date"],
            expired_product["product_name"],
            str(expired_product["quantity"]),
        )
        
    console.print(expired_table)
