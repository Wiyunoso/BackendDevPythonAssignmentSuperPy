# Report Project Superpy

## READABILITY & STRUCTURE

I paid attention to the readability of the code through the eyes of a programmer. I started with putting the code of the main functionalities all in one "main_functions.py" file. Whilst programming I encounterd a lot of scrolling, looking for the relevant function. With putting the main functionalities into separate py-files, the 'skeleton' of the programm is more visibile, enhancing the readability and reducing the amount of scrolling.

The flow of each functiontionality or its logarithm, is backed up with quite some comments, explaining in human language what the following block of code or simply one line of coding does.

Though I am satisfied with the current readability and structure for myself, and hopefully also for another programmer, I wonder how much more effective, cleaner and readable the programm would have been if I have taken more us of "classes" and "objects". I have only applied "classes" in the test.py-file where I needed to create an args-object in order to load parameters into the main-functions instead of the parsers providing them from the CLI entries.

## SELL & SET_DATE FUNCTION & LIST.COPY()

The two most complex functionality-flows are in the sell- and set_date-function.

### sell
My requirement for selling was that the Id for each sold product, would still be visible in the sales-records, so that it can be traced back when needed.
That made the handling of the amount of each sale, with the availabe amounts under different Id's in inventory, complex.

For example the handling of a left-over in the amount of sale, as a sale_amount certainly does not always have an incidental, exact match with a sum of availabe amounts with different Id's in the inventory:

```python
                else: # ie: sale_counter < stock_quantity_in_row
                    # entering this "else"-body means there is a left-over in the sale_amount_counter (as the amount of a sale certainly does not always have an incidental, exact match with a sum of buy-quantity-registrations).
                    # the quantity of the left-over in sale_counter must also be registrated in the soldCSV file:
                    inventory_product["quantity"] = sale_counter
                    add_product_to_csv(
                        sold_csv_file,
                        inventory_product["Id"],
                        inventory_product["product_name"],
                        inventory_product["quantity"],
                        inventory_product["expiration_date"],
                        "no_buy_date_needed",
                        "no_buy_price_needed",
                        args.sales_price,
                    )  # the quantity of the'stock_quantity_in_row' must be deducted with the amount left-over in sale_counter. The new 'inventory_product['quantity'] will be written to inventoryCSV-file in the if...else-body below, when the adjusted inventory_list is looped:
                    inventory_product["quantity"] = stock_quantity_in_row - sale_counter
                    sale_counter -= stock_quantity_in_row  # sale_counter still must be adjusted, otherwise the check if there is more quantity input in 'sell' than there is available in inventory, will not be handled correctly in the next 'if..., else' statement.
                    console.print(
                        f"You have succesfully sold {args.quantity} items of '{args.product_name}'.",
                        style="green",
                    )
                    break
```
### set_date
With the set_date function the date which the program perceives as 'today', may be set to a date in the past. 
In such case, there is also the possibility to sell (and buy) things in the past, and thereby changing the inventory of the past. The already registrated sales counting from that new date on, are therefore not valid anymore, as they were based on an inventory before the change. 
Id est: when adding a sale in the past, the already registrated sale later may not be possible anymore, because that product may be already out of stock due to that newly added sale in the past.
Therefore, when setting the current date in the past, the sales registration will be undone till that new date in the past.

I wanted to warn the user about this deleting of sales-registrations before he/she proceeds. I solved this by simply adding an input() function:

```python
        if new_date_obj < previous_current_date_obj: # ie: setting a date in the paset
            console.print(
                f"This date is prior to the current date of the programm. If you proceed, the registration of the products which were where sold or expired between this current date and the newly set date will be undone in order to have an accurate inventory, due to the possibility to entry sales on this newly set date. \nAre your sure you want to proceed? Entry with 'y' or 'n'.",
                style="red",
            )
            answer = input().lower()

            if answer == "y" or answer == "yes":
                console.print(f"Current date is set to: {new_date_obj.date()}", style="green")
                # write the given date as the current date in the text-file
                with open("current_date.txt", "r+") as current_date_file:
                    current_date_file.write(new_date_obj.strftime("%Y-%m-%d"))
                # adjust the inventory, expired and CSV to the new current date
                adjust_inventory_expired_and_sold_CSV(previous_current_date_obj, new_date_obj)
            else:
                display_start_menu()
                return
``` 
### list.copy()
Originally, there were two list-loopings in the code where the list is adjusted while still going through its loop. (In the sell-function and remove_product_from_CSV.) I encountered an incorrect output with that. 
I found out (by inserting print-statements in the loop o.a.) that removing an item from a list, while being looped, messes up its sequence.
I solved this by creating a copy of the list to loop over with, while removing an item from the original list and using the latter list as outcome.

```python
def remove_product_from_CSV(Id, csv_file):
    with open(csv_file, "r", newline="") as file:
        file_list = list(csv.DictReader(file))
        file_list_copy = file_list.copy()
    for product in file_list_copy:
        if Id == product["Id"]:
            file_list.remove(product)

    write_csv_file(csv_file, file_list)
```
## SUB-FUNCTIONS
I started  off with separating sub-functions from main-functions to enhance readability of the flow of a main-function.
I define sub-function with: basic functions which supports a main-function and may be re-used in other functions. 
By technically defining them into a seperate file, the code of the main-function will be shortened and not diffused by code which is not directly a key in comprehending the logarithm of the main-function.

An example of a sub-function is add_product_to_csv():

```python
def add_product_to_csv(csv_file, Id, product_name, quantity, expiration_date, buy_date="", buy_price=0, sales_price=0,):
    with open(csv_file, "r", newline="") as file:
        products_list = list(csv.DictReader(file))

        if csv_file == bought_csv_file:
            products_list.append(<<code assigning values to bought_csv_file>>)

            # sort the bought_products by buy_date
            products_list.sort(key=lambda row: datetime.datetime.strptime(row["buy_date"], "%Y-%m-%d"))
        elif csv_file == inventory_csv_file or csv_file == expired_csv_file:
            products_list.append(<<code assigning values to expired_csv_file>>)
            ...
        elif csv_file == sold_csv_file:
            ...
        write_csv_file(csv_file, products_list)
```

At first I declared add_product_to_csv()-functions for each csv-file separately as they have their own sets of parameters. But by setting the csv-file as a parameter and by giving the unique parameters default values in the declaration of this function, I can combine them into one function, again enhancing readability and reducing scrolling. This way, parameters which are set with default values simply do not necessarlily have to be provided when calling this function.

By declaring them as generic as possible, they become more potentially re-usable for supporting different (main)functions and algorithms. 
Like the last function called above: "write_csv_file(csv_file, products_list)" which is used in this add_product_to_csv()-function as well other functions, reducing replicates of code.
Centralizing them into a function makes them also more effective in making changes to that code, as you only have to adjust in this central point instead of adjusting them one by one in each replicate.

