# Imports
from argparse import *
from parsers import create_parser
from rich.console import Console
from set_and_advance_date import (
    set_date_and_adjust_inventory_expired_and_sold_CSV,
    advance_date_and_adjust_inventory_expired_and_sold_CSV,
    display_start_menu,
)
from buy import buy_product
from sell import sell_product
from report import report_inventory, report_revenue, report_profit, report_expired_products
from export_to_excell import export_to_excell
from test.test import clear_csv_files, test_main_functionalities_with_demo_data

import sys

sys.path.insert(0, "./test")


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

console = Console()


def main():
    parser = create_parser()
    args = parser.parse_args()

    if (
        args.set_date
    ):  # # apparently, the parser recognise args.set_date, though it was defined as 'set-date'
        set_date_and_adjust_inventory_expired_and_sold_CSV(args.set_date)
    elif args.advance_date:
        advance_date_and_adjust_inventory_expired_and_sold_CSV(args.advance_date)
    elif args.function == "buy":
        buy_product(args)
    elif args.function == "sell":
        sell_product(args)
    elif args.function == "report":
        if args.type_of_report == "inventory" and bool(args.date) == True:
            report_inventory(args.date)
        elif args.type_of_report == "inventory":
            report_inventory()
        elif args.type_of_report == "revenue":
            report_revenue(args.date_1, args.date_2)
        elif args.type_of_report == "profit":
            report_profit(args.date_1, args.date_2)
        elif args.type_of_report == "expired":
            report_expired_products()
        else:
            console.print(
                "Specify further with typing 'inventory', 'revenue' or 'profit' after 'report'.",
                style="red",
            )
    elif args.function == "export_to_excell":
        if args.file_to_export == "inventory":
            export_to_excell("inventory")
        elif args.file_to_export == "bought":
            export_to_excell("bought")
        elif args.file_to_export == "sold":
            export_to_excell("sold")
        elif args.file_to_export == "expired":
            export_to_excell("expired")
        else:
            console.print(
                "Specify further with typing 'inventory', 'bought', 'sold' or 'expired' after 'export_to_excell'.",
                style="red",
            )
    elif args.function == "test_function":
        if args.function_to_test == "set_date":
            test_main_functionalities_with_demo_data("set_date")
        elif args.function_to_test == "advance_date":
            test_main_functionalities_with_demo_data("advance_date")
        elif args.function_to_test == "buy":
            test_main_functionalities_with_demo_data("buy")
        elif args.function_to_test == "sell":
            test_main_functionalities_with_demo_data("sell")
        elif args.function_to_test == "report_revenue":
            test_main_functionalities_with_demo_data("report_revenue")
        elif args.function_to_test == "report_profit":
            test_main_functionalities_with_demo_data("report_profit")
        else:
            console.print(
                "Specify further with typing 'set_date', 'buy', 'sell', 'report_revenue' or 'report_profit' after 'test_function'.",
                style="red",
            )
    elif args.function == "clear_csv_files":
        clear_csv_files()
    else:
        display_start_menu()


if __name__ == "__main__":
    main()
