import argparse
from rich.console import Console


def create_parser():
    main_parser = argparse.ArgumentParser(
        description="Welcome to the SuperPy Supermarket Tool!",
        epilog="Thank you for using the Superpy Supermarket Tool!",
    )

    main_parser.add_argument(
        "-sd",
        "--set-date",
        help="Type '-sd', followed by the desired date (YYYY-MM-DD) to set the desired date to be used as 'current date' in this programme.",
    )

    main_parser.add_argument(
        "-ad",
        "--advance-date",
        help="Type '-ad', followed by the number of days you want to advance the current date of the programme.",
    )

    subparsers = main_parser.add_subparsers(dest="function", title="functions")

    buy_parser = subparsers.add_parser(
        "buy",
        help="Type 'buy' to buy a product. Specify further with 'productname', 'quantity', 'purchase price' and 'expiration date' (YYYY-MM-DD).",
    )
    buy_parser.add_argument(
        "product_name", type=str, help="Type the name of the purchased product."
    )
    buy_parser.add_argument(
        "quantity",
        type=int,
        help="Type the quantity of the purchased product (in sales-units).",
    )
    buy_parser.add_argument(
        "buy_price",
        type=float,
        help="Type the purchasing price of the product (only numbers).",
    )
    buy_parser.add_argument(
        "expiration_date",
        help="Type the expiration-date of the purchased product, following YYYY-MM-DD.",
    )

    sell_parser = subparsers.add_parser(
        "sell",
        help="Type 'sell' to sell a product. Specify further with 'product name', 'quantity sold', and 'sales price'.",
    )
    sell_parser.add_argument("product_name", help="Type the name of the product sold.")
    sell_parser.add_argument(
        "quantity",
        type=int,
        help="Type in the quantity of the product sold (in sales-units).",
    )
    sell_parser.add_argument(
        "sales_price", help="Type in the selling price of the product."
    )

    reports_parser = subparsers.add_parser(
        "report",
        help="Type 'report' to create an inventory, revenue or profit report. Specify further with 'inventory', 'revenue' or 'profit'.",
    )
    reports_subparsers = reports_parser.add_subparsers(
        dest="type_of_report", title="Type of report"
    )

    inventory_parser = reports_subparsers.add_parser(
        "inventory",
        help="Type in 'inventory' to report inventory. Optional to add date for a report of the desired date, by typing in addition '--date YYYY-MM-DD'.",
    )
    inventory_parser.add_argument(
        "--date",
        help="Type in the desired date of the inventory, following the format YYYY-MM-DD.",
    )

    revenue_parser = reports_subparsers.add_parser(
        "revenue",
        help="Type in 'revenue' followed by a start-date and an end-date of the revenue-report, following YYYY-MM-DD.",
    )

    revenue_parser.add_argument(
        "date_1", help="Type in the date on which the revenue-report should start."
    )

    revenue_parser.add_argument(
        "date_2", help="Type in the final date of the revenue-report."
    )

    profit_parser = reports_subparsers.add_parser(
        "profit",
        help="Type in 'profit' followed by a start-date and an end-date of the profit-report.",
    )
    profit_parser.add_argument(
        "date_1", help="Type in the date on which the profit-report should start."
    )

    profit_parser.add_argument(
        "date_2", help="Type in the final date of the profit-report."
    )
    expired_parser = reports_subparsers.add_parser(
        "expired", help="Type in 'expired' to report the current expired products."
    )

    expired_parser.add_argument(
        'no_arguments_required_with_nargs="*"',
        nargs="*",
        help="Type 'clear-csv-files' to clear all registrations in all CSV files.",
    )

    export_to_excell_parser = subparsers.add_parser(
        "export_to_excell",
        help="Type in 'export_to_excell' to export a CSV-file to Excell. Specify further with 'inventory', 'bought', 'sold' or 'expired'.",
    )
    export_to_excell_subparsers = export_to_excell_parser.add_subparsers(
        dest="file_to_export", title="Which file to export?"
    )

    inventory_excell_parser = export_to_excell_subparsers.add_parser(
        "inventory", help="Typing this will export the inventory.csv to Excell."
    )
    bought_excell_parser = export_to_excell_subparsers.add_parser(
        "bought", help="Typing this will export the bought.csv to Excell."
    )
    sold_excell_parser = export_to_excell_subparsers.add_parser(
        "sold", help="Typing this will export the sold.csv to Excell."
    )
    expire_excell_parser = export_to_excell_subparsers.add_parser(
        "expired", help="Typing this will export the expire.csv to Excell."
    )
    test_parser = subparsers.add_parser(
        "test_function",
        help="Type in 'test_functions' to test the main functions of this program. Specify further with 'set_date', 'buy', 'sell','report revenue' or 'report profit'. The test of 'report inventory' is already included in the 'set-date'-, 'buy'- and 'sell'-test.",
    )
    test_subparsers = test_parser.add_subparsers(
        dest="function_to_test", title="Which function to test?"
    )

    test_set_date_parser = test_subparsers.add_parser(
        "set_date", help="Typing 'set_date' will test the set-date function."
    )
    test_advance_date_parser = test_subparsers.add_parser(
        "advance_date",
        help="Typing 'advance_date' will test the advance-date function.",
    )
    test_buy_parser = test_subparsers.add_parser(
        "buy", help="Typing 'buy' will test the set-date function."
    )
    test_sell_parser = test_subparsers.add_parser(
        "sell", help="Typing 'sell' will test the sell function."
    )
    test_report_revenue = test_subparsers.add_parser(
        "report_revenue",
        help="Typing 'report revenue' will test the report-revenue function.",
    )
    test_report_profit = test_subparsers.add_parser(
        "report_profit",
        help="Typing 'report profit' will test the report-revenue function.",
    )
    clear_csv_files_parser = subparsers.add_parser(
        "clear_csv_files",
        help="Type 'clear_csv_files' to clear all registrations in all CSV files.",
    )

    clear_csv_files_parser.add_argument(
        'no_arguments_required_with_nargs="*"',
        nargs="*",
        help="Type 'clear-csv-files' to clear all registrations in all CSV files.",
    )

    return main_parser
