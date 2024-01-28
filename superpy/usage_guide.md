# USAGE GUIDE SUPERPY SUPERMARKET TOOL

The SuperPy Supermarket Tool (SPST) is a Command Line Interface (CLI) tool, designed to enter buy and sale registrations, monitor inventory and keep track of expired products. These data will be stored in specified CSV-files with the possibility to export them to Excell-files. Furthermore, it has the functionality to generate revenue and profit reports.

This document will guide you throught its usage.

With the CLI on the correct path where SPST is installed, type in: "python main.py" or "py main.py".
The startmenu will display as found at the end of this document.

## FUNCTIONS WITH EXAMPLES
It shows the several functions and the instructions to execute them.
To clarify, some functions with its instructions are shown with an example of entries in the CLI.


  buy     Type 'buy' to buy a product. Specify further with 'productname', 'quantity', 'purchase price' and 'expiration date' (YYYY-MM-DD).
Example: ...\superpy> py main.py buy orange 3 2.50 2024-04-04

  sell    Type 'sell' to sell a product. Specify further with 'product name', 'quantity sold', and 'sales price'.
Example: ...\superpy> py main.py sell orange 1 3.50

  report  Type 'report' to create an inventory, revenue or profit report. Specify further with 'inventory', 'revenue' or 'profit'.
Example: ...\superpy> py main.py report profit

## ARGUMENTS
Some functions require further arguments, like the report profit function. When not provided, the CLI will raise an error message and will inform about further instructions.
In the case of latter example of the report profit function:

main.py report profit: error: the following arguments are required: date_1, date_2

Example complete entries for report profit: ...\superpy> py main.py report profit 2023-01-01 2024-01-01

## HELP
For further explanation of an argument, one can type in '--help' or '-h' straight after it. This will open the help-text.

Example: ...\superpy> py main.py report profit -h

Result: usage: main.py report profit [-h] date_1 date_2
        positional arguments: 
        date_1      Type in the date on which the profit-report should start.
        date_2      Type in the final date of the profit-report

## USAGE
"usage:" shows the entries needed in the CLI for that function.
The "usage" in the startmenu shows:
usage: main.py [-h] [-sd SET_DATE] [-ad ADVANCE_DATE] {buy,sell,report,export_to_excell,test_function,clear_csv_files} ...

The functions in the curly brackets {} shows the main functions, while in square brackets [] are the somewhat the 'hidden' optional features of this tool and not required to entry. You can excess its functionaly by typing the '-text'.

Example: ...\superpy> py main.py -sd 1999-01-01

## SET_DATE FUNCTION
The example above will set the day, SPST perceives as 'today' (the current day) to 1st of Jan 1999. Therefore the 'set_date' function makes buy- and sale-entries possible in the "past" and "future" (also possible with the 'advance_date' feature).
!!!!!!!!
  Since selling in the past is possible, the inventory of the past will change with it. The already registrated sales counting from that new date on, are therefore not valid anymore, as they were based on an inventory before the changes. 
  Id est: when adding a sale in the past, the already registrated sale later may not be possible anymore, because that product may be already out of stock due to that newly added sale in the past.
  Therefore, when setting the current date in the past, the sales registration will be undone till that new date in the past.
  This warning will also be given when setting the current date in the past and the CLI will ask to proceed or not.
!!!!!!!!
  Sales registration will not be deleted when asking for an inventory report from the past with the report inventory function. Since this won't set the current date to the past, and therefore no possibility to sell in the past, it's not necessary and not desirable to delete sales registration.

## STATIC EXCELL FILES
While the inventory.csv is dynamic: updated to a changing current date, the excell files are not. The data in those files remain static to the date the files were initiated and won't update with a changing current date. To update them to the current day, one can perform the export_to_excell function for each Excell file.

## TEST_FUNCTION AND CLEAR_CSV_FILES
For an administrator of this tool to test or simply to serve as a user-demo, one can start up the test_function. It will load some pre-set demo data in the function one would like to test. With alternating between setting or advancing the date manually in the SPST (or using the pre-set data in the test-function) and/or repeating the test_function buy and/or test_function sell, one can observe the changes made in SPST.

While in the regular buy and sell function only a line of text will confirm its execution, for visualisation purposes, the report_inventory function is attached all the test-functions. 

-------------------------------------------------------------------------------------------------------------------------------------------

STARTMENU
options:
  -h, --help            show this help message and exit
  -sd SET_DATE, --set-date SET_DATE
                        Type '-sd', followed by the desired date (YYYY-MM-DD) to set the desired date to be used as 'current date' in this programme.
  -ad ADVANCE_DATE, --advance-date ADVANCE_DATE
                        Type '-ad', followed by the number of days you want to advance the current date of the programme.

functions:
  {buy,sell,report,export_to_excell,test_function,clear_csv_files}
    buy                 Type 'buy' to buy a product. Specify further with 'productname', 'quantity', 'purchase price' and 'expiration date' (YYYY-MM-DD).
    sell                Type 'sell' to sell a product. Specify further with 'product name', 'quantity sold', and 'sales price'.
    report              Type 'report' to create an inventory, revenue or profit report. Specify further with 'inventory', 'revenue' or 'profit'.
    export_to_excell    Type in 'export_to_excell' to export a CSV-file to Excell. Specify further with 'inventory', 'bought', 'sold' or 'expired'
    test_function       Type in 'test_functions' to test the main functions of this program. Specify further with 'set_date', 'buy', 'sell','report revenue' or 'report       
                        profit'. The test of 'report inventory' is already included in the 'set-date'-, 'buy'- and 'sell'-test.
    clear_csv_files     Type 'clear_csv_files' to clear all registrations in all CSV files.