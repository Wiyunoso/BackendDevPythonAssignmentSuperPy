import json
from rich.console import Console

from set_and_advance_date import (
    set_date_and_adjust_inventory_expired_and_sold_CSV,
    advance_date_and_adjust_inventory_expired_and_sold_CSV,
)
from report import report_inventory, report_revenue, report_profit
from buy import buy_product
from sell import sell_product

from sub_functions import get_current_date, write_csv_file

console = Console()


class test_buy_args_object:
    def __init__(self, product_name, quantity, buy_price, expiration_date):
        self.product_name = product_name
        self.quantity = quantity
        self.buy_price = buy_price
        self.expiration_date = expiration_date

    def __str__(self):
        return f"{self.product_name},{self.expiration_date})"


class test_sell_args_object:
    def __init__(self, product_name, quantity, sales_price):
        self.product_name = product_name
        self.quantity = quantity
        self.sales_price = sales_price

    def __str__(self):
        return f"{self.product_name},{self.expiration_date})"


def test_main_functionalities_with_demo_data(functionality):
    test_data_file = open("./test/test_data.json")
    test_data = json.load(test_data_file)

    console = Console()

    if functionality == "set_date":
        for item in test_data["set_date"]:
            set_date_and_adjust_inventory_expired_and_sold_CSV(item["new_date"])
            report_inventory(item["new_date"])
    elif functionality == "advance_date":
        for item in test_data["advance_date"]:
            advance_date_and_adjust_inventory_expired_and_sold_CSV(item["number"])
            report_inventory(get_current_date("string"))
    elif functionality == "buy":
        for item in test_data["buy"]:
            args = test_buy_args_object(
                item["product_name"],
                item["quantity"],
                item["buy_price"],
                item["expiration_date"],
            )
            buy_product(args)
            report_inventory(get_current_date("string"))

    elif functionality == "sell":
        for item in test_data["sell"]:
            args = test_sell_args_object(
                item["product_name"],
                item["quantity"],
                item["sales_price"],
            )
            sell_product(args)
            report_inventory(get_current_date("string"))
    elif functionality == "report_revenue":
        for item in test_data["report_revenue"]:
            report_revenue(item["date1"], item["date2"])
    elif functionality == "report_profit":
        for item in test_data["report_profit"]:
            report_profit(item["date1"], item["date2"])
    else:
        console.print(
            f"Type in a correct function: 'set_date', 'buy','sell','report_revenue' or 'report_profit'.",
            style="red",
        )


def clear_csv_files():
    list = []
    write_csv_file("./csv_files/bought.csv", list)
    write_csv_file("./csv_files/inventory.csv", list)
    write_csv_file("./csv_files/expired.csv", list)
    write_csv_file("./csv_files/sold.csv", list)
    console.print(f"All the csv-files are cleared now.", style="green")
