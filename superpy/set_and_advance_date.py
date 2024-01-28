import datetime
from rich.console import Console
from parsers import *
import csv
from sub_functions import (
    get_current_date,
    print_current_day_message,
    add_product_to_csv,
    write_csv_file,
    remove_product_from_CSV,
    get_info_from_product_from_CSV_using_Id,
)

bought_csv_file = "./csv_files/bought.csv"
inventory_csv_file = "./csv_files/inventory.csv"
expired_csv_file = "./csv_files/expired.csv"
sold_csv_file = "./csv_files/sold.csv"

console = Console()


def set_date_and_adjust_inventory_expired_and_sold_CSV(new_date_string):
    previous_current_date_obj = get_current_date("object")

    try:  # check if a valid date is given, otherwise print notification
        new_date_obj = datetime.datetime.strptime(new_date_string, "%Y-%m-%d")

        if new_date_obj < previous_current_date_obj:  # ie: setting a date in the past
            console.print(
                f"This input-date ({new_date_string}) is prior to the current date ({get_current_date('string')}) of the programm. If you proceed, the registration of the products which were where sold or expired between this current date and the newly set date will be undone in order to have an accurate inventory, due to the possibility to entry sales on this newly set date. \nAre your sure you want to proceed? Entry with 'y' or 'n'.",
                style="red",
            )
            answer = input().lower()

            if answer == "y" or answer == "yes":
                console.print(
                    f"Current date is set to: {new_date_obj.date()}", style="green"
                )

                # write the given date as the current date in the text-file
                with open("current_date.txt", "r+") as current_date_file:
                    current_date_file.write(new_date_obj.strftime("%Y-%m-%d"))
                # adjust the inventory, expired and CSV to the new current date
                adjust_inventory_expired_and_sold_CSV(
                    previous_current_date_obj, new_date_obj
                )
            else:
                display_start_menu()
                return
        elif new_date_obj >= previous_current_date_obj:
            console.print(
                f"Current date is set to: {new_date_obj.date()}", style="green"
            )

            # write the given date as the current date in the text-file
            with open("current_date.txt", "r+") as current_date_file:
                current_date_file.write(new_date_obj.strftime("%Y-%m-%d"))
            # adjust the inventory, expired and CSV to the new current date
            adjust_inventory_expired_and_sold_CSV(
                previous_current_date_obj, new_date_obj
            )

    except ValueError:
        console.print(
            "Invalid date format. Please provide the date following YYYY-MM-DD.",
            style="red",
        )


def display_start_menu():
    parser = create_parser()
    print_current_day_message()
    parser.print_help()
    print_current_day_message()


def adjust_inventory_expired_and_sold_CSV(previous_current_date_obj, new_date_obj):
    with open(bought_csv_file, "r", newline="") as bought_file:
        bought_list = list(csv.DictReader(bought_file))
        # bought_file.seek(0)

    if new_date_obj > previous_current_date_obj:
        #  summary:
        # NEW INVENTORY = CURRENT INVENTORY + BOUGHT PRODUCTS - EXPIRED PRODUCTS

        # 1) When the new_date lies after the current date: add bought products to the inventory with a buy-date between the current_date and the new_date or equal to the new_date. (For they have been deducted before, when the current_date was set to a date prior to their buy-date.)

        for bought_product in bought_list:
            buy_date = datetime.datetime.strptime(
                bought_product["buy_date"], "%Y-%m-%d"
            )

            if previous_current_date_obj < buy_date and buy_date <= new_date_obj:
                add_product_to_csv(
                    inventory_csv_file,
                    bought_product["Id"],
                    bought_product["product_name"],
                    bought_product["quantity"],
                    bought_product["expiration_date"],
                    bought_product["buy_date"],
                )
        # 2a): remove the expired products from inventoryCSV and 2b): add them to expired.csv if the new_date is ahead of the current_date:

        with open(inventory_csv_file, "r", newline="") as inventory_file:
            inventory_list = list(csv.DictReader(inventory_file))

        for inventory_product in inventory_list:
            if new_date_obj > datetime.datetime.strptime(
                inventory_product["expiration_date"], "%Y-%m-%d"
            ):
                remove_product_from_CSV(inventory_product["Id"], inventory_csv_file)
                add_product_to_csv(
                    expired_csv_file,
                    inventory_product["Id"],
                    inventory_product["product_name"],
                    inventory_product["quantity"],
                    inventory_product["expiration_date"],
                    inventory_product["buy_date"],
                )

    elif new_date_obj == previous_current_date_obj:
        pass
    else:  # new_date_obj < previous_current_date_obj:
        # Summary:
        # NEW INVENTORY = CURRENT INVENTORY - BOUGHT PRODUCTS between new and current date + SOLD AND EXPIRED PRODUCTS bought before new_date.

        # When the new_date is prior to the current_date: the products bought between the new_date and the current date must be removed from the inventory.csv, the sold.csv and the expired.csv. (For those are the files where those products are split to.)

        for bought_product in bought_list:
            buy_date = datetime.datetime.strptime(
                bought_product["buy_date"], "%Y-%m-%d"
            )
            if new_date_obj < buy_date and buy_date <= previous_current_date_obj:
                remove_product_from_CSV(bought_product["Id"], inventory_csv_file)
                remove_product_from_CSV(bought_product["Id"], sold_csv_file)
                remove_product_from_CSV(bought_product["Id"], expired_csv_file)

        # now the csv-files are cleaned from the products which are bought in the in-between period, the left-over actions performed on the inventory-file (on the products which are bought before the new_date) must be undone. (I.e. products which are bought before the new_date, and sold or expired in that in-between period, must be undone and return to the inventory.csv)

        with open(inventory_csv_file, "r", newline="") as inventory_file:
            inventory_list = list(csv.DictReader(inventory_file))

        with open(expired_csv_file, "r", newline="") as expired_products_file:
            expired_products_list = list(csv.DictReader(expired_products_file))

        for expired_product in expired_products_list:
            if new_date_obj <= datetime.datetime.strptime(
                expired_product["expiration_date"], "%Y-%m-%d"
            ):
                remove_product_from_CSV(expired_product["Id"], expired_csv_file)
                inventory_list.append(expired_product)

        # when expiring, a row in inventary will be transferred to expired.csv in its whole and vice versa. Therefore there is no need to check for another row with the same Id.
        # with open(inventory_csv_file, "r", newline="") as inventory_file:
        #     inventory_list = list(csv.DictReader(inventory_file))

        with open(sold_csv_file, "r", newline="") as sold_file:
            sold_products_list = list(csv.DictReader(sold_file))

        for sold_product in sold_products_list:
            if new_date_obj < datetime.datetime.strptime(
                sold_product["sales_date"], "%Y-%m-%d"
            ):
                # a product with the same Id, may occur more than once in the sold.csv due to different sale moments. When transferring it back to inventory it's more neat to combine them into one row as they have the same Id.
                found = False
                for inventory_product in inventory_list:
                    if inventory_product["Id"] == sold_product["Id"]:
                        found = True
                        remove_product_from_CSV(sold_product["Id"], sold_csv_file)
                        inventory_product["quantity"] = int(
                            inventory_product["quantity"]
                        ) + int(sold_product["quantity"])
                        break
                        # since an Id only occurs once in inventory, the loop might as well be broken, once Id is found
                inventory_list.sort(
                    key=lambda row: datetime.datetime.strptime(
                        row["expiration_date"], "%Y-%m-%d"
                    )
                )
                # in the following case all items of a buy is sold, therefore not found in inventory, but nevertheless still need to be added to the inventory
                if found == False:
                    Id = sold_product["Id"]
                    conversion_sold_to_inventory = {
                        "expiration_date": get_info_from_product_from_CSV_using_Id(
                            Id, bought_csv_file, "expiration_date"
                        ),
                        "Id": sold_product["Id"],
                        "buy_date": get_info_from_product_from_CSV_using_Id(
                            Id, bought_csv_file, "buy_date"
                        ),
                        "product_name": sold_product["product_name"],
                        "quantity": sold_product["quantity"],
                    }
                    inventory_list.append(conversion_sold_to_inventory)
                    remove_product_from_CSV(sold_product["Id"], sold_csv_file)

        write_csv_file(inventory_csv_file, inventory_list)


def advance_date_and_adjust_inventory_expired_and_sold_CSV(number_of_days):
    # get the current date, advance it and set the new current date
    try:
        advanced_date = get_current_date("object") + datetime.timedelta(
            days=int(number_of_days)
        )
        set_date_and_adjust_inventory_expired_and_sold_CSV(
            advanced_date.strftime("%Y-%m-%d")
        )
    except ValueError:
        console.print("Invalid entry. Please type a number.", style="red")
