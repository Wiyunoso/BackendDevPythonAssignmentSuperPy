import datetime
import csv
from sub_functions import (
    get_current_date,
    add_product_to_csv
)
from rich.console import Console

console = Console()

bought_csv_file = "./csv_files/bought.csv"
inventory_csv_file = "./csv_files/inventory.csv"


def buy_product(args):
    with open(bought_csv_file, "r+", newline="") as bought_file:
        bought_products_list = list(csv.DictReader(bought_file))
        Id = len(bought_products_list) + 1

    buy_date = get_current_date("string")

    expiration_date_object = datetime.datetime.strptime(
        args.expiration_date, "%Y-%m-%d"
    )
    buy_date_object = datetime.datetime.strptime(buy_date, "%Y-%m-%d")

    if expiration_date_object < buy_date_object:
        console.print(
            f"This product '{args.product_name}' with expiry date'{args.expiration_date}' is already expired and therefore cannot be bought.",
            style="red",
        )
    else:
        add_product_to_csv(
            bought_csv_file,
            Id,
            args.product_name,
            args.quantity,
            args.expiration_date,
            buy_date,
            args.buy_price,
        )
        add_product_to_csv(
            inventory_csv_file,
            Id,
            args.product_name,
            args.quantity,
            args.expiration_date,
            buy_date,
        )
        console.print(
            f"{args.quantity} items of '{args.product_name}' are succesfully added to the bought.csv-file and inventory.csv-file",
            style="green",
        )
