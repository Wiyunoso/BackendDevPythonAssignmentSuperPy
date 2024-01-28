import datetime
import csv
from random import sample
from rich.console import Console

bought_csv_file = "./csv_files/bought.csv"
inventory_csv_file = "./csv_files/inventory.csv"
expired_csv_file = "./csv_files/expired.csv"
sold_csv_file = "./csv_files/sold.csv"

console = Console()


def add_product_to_csv(
    csv_file,
    Id,
    product_name,
    quantity,
    expiration_date,
    buy_date="",
    buy_price=0,
    sales_price=0,
):
    with open(csv_file, "r", newline="") as file:
        products_list = list(csv.DictReader(file))
        file.seek(0)

        if csv_file == bought_csv_file:
            products_list.append(
                {
                    "Id": Id,
                    "buy_date": buy_date,
                    "product_name": product_name,
                    "quantity": quantity,
                    "buy_price": buy_price,
                    "expiration_date": expiration_date,
                }
            )
            # sort the bought_products by buy_date
            products_list.sort(
                key=lambda row: datetime.datetime.strptime(row["buy_date"], "%Y-%m-%d")
            )
        elif csv_file == inventory_csv_file or csv_file == expired_csv_file:
            products_list.append(
                {
                    "expiration_date": expiration_date,
                    "Id": Id,
                    "buy_date": buy_date,
                    "product_name": product_name,
                    "quantity": quantity,
                }
            )
            # sort the list by expiration_date
            products_list.sort(
                key=lambda row: datetime.datetime.strptime(
                    row["expiration_date"], "%Y-%m-%d"
                )
            )
        elif csv_file == sold_csv_file:
            products_list.append(
                {
                    "Id": Id,
                    "sales_date": get_current_date("string"),
                    "product_name": product_name,
                    "quantity": quantity,
                    "sales_price": sales_price,
                }
            )
            # sort the sold_products by sales_date
            products_list.sort(
                key=lambda row: datetime.datetime.strptime(
                    row["sales_date"], "%Y-%m-%d"
                )
            )

        write_csv_file(csv_file, products_list)


def remove_product_from_CSV(Id, csv_file):
    with open(csv_file, "r", newline="") as file:
        file_list = list(csv.DictReader(file))
        file_list_copy = file_list.copy()
    for product in file_list_copy:
        if Id == product["Id"]:
            file_list.remove(product)

    write_csv_file(csv_file, file_list)


def write_csv_file(csv_file, csv_file_list):
    with open(csv_file, "w", newline="") as file:
        if csv_file == bought_csv_file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "Id",
                    "buy_date",
                    "product_name",
                    "quantity",
                    "buy_price",
                    "expiration_date",
                ],
            )
        elif csv_file == inventory_csv_file or csv_file == expired_csv_file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "expiration_date",
                    "Id",
                    "buy_date",
                    "product_name",
                    "quantity",
                ],
            )
        elif csv_file == sold_csv_file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "Id",
                    "sales_date",
                    "product_name",
                    "quantity",
                    "sales_price",
                ],
            )
        writer.writeheader()
        writer.writerows(csv_file_list)


def get_current_date(type):
    with open("current_date.txt", "r") as current_date_file:
        if type == "string":
            date = current_date_file.read()
            if not date:  # Return today's date as default if file is empty
                return datetime.date.today().strftime("%Y-%m-%d")
            return date
        elif type == "object":
            date = datetime.datetime.strptime(current_date_file.read(), "%Y-%m-%d")
            if not date:  # Return today's date as default if file is empty
                return datetime.date.today("%Y-%m-%d")
            return date


def get_info_from_product_from_CSV_using_Id(Id, csv_file, info):
    with open(csv_file, "r", newline="") as file:
        product_list = list(csv.DictReader(file))

        for product in product_list:
            if product["Id"] == Id:
                return product[info]


def list_of_rows_and_sum_of_multiplication_from_2_columns_from_specified_CSV_over_specified_period(
    date_1, date_2, date_column, csv_file, column_1, column_2
):
    date_1_obj = datetime.datetime.strptime(date_1, "%Y-%m-%d")
    date_2_obj = datetime.datetime.strptime(date_2, "%Y-%m-%d")
    count = 0.00
    with open(csv_file) as file:
        items = list(csv.DictReader(file))
        items_list_of_specified_period_plus_row_multiplication = []

        for item in items:
            if (
                datetime.datetime.strptime(item[date_column], "%Y-%m-%d") >= date_1_obj
                and datetime.datetime.strptime(item[date_column], "%Y-%m-%d")
                <= date_2_obj
            ):
                row_multiplication = float(item[column_1]) * float(item[column_2])
                item["row_multiplication"] = row_multiplication
                items_list_of_specified_period_plus_row_multiplication.append(item)
                count += row_multiplication
    return (count, items_list_of_specified_period_plus_row_multiplication)


def print_current_day_message():
    current_date = get_current_date("string")
    console.print(
        f"THE CURRENT DATE OF THIS PROGRAM IS SET TO {current_date}! Type '--set-date'('-sd') or '--advance-date'('-ad') to change it.",
        style="red on white",
    )
