import csv
from rich.console import Console
from sub_functions import add_product_to_csv, write_csv_file

inventory_csv_file = "./csv_files/inventory.csv"
sold_csv_file = "./csv_files/sold.csv"

console = Console()


def sell_product(args):
    # only allowed to sell a product as much as there is in stock."
    # start selling the ones with the shortes shelve-life first.
    """
    A sale of a certain amount of a product may consists of different "Id's" of the product (due to different buy- and expiration-dates).
    Each sale of an "Id" will be recorded separtely in the sold.csv.
    """

    sale_counter = int(args.quantity)
    in_stock = False
    stock_counter = 0

    with open(inventory_csv_file, "r") as inventory_file:
        inventory_list = list(csv.DictReader(inventory_file))

        inventory__list_copy = inventory_list.copy()
        # removing an item from a list, which is being looped, messes up its sequence, hence creating a copy of the list to loop over with, while removing an item from the original list

        for inventory_product in inventory__list_copy:
            # check whether there is stock
            if inventory_product["product_name"] == args.product_name:
                in_stock = True
                stock_quantity_in_row = int(inventory_product["quantity"])
                stock_counter += stock_quantity_in_row
                # sell out the stock with the shortest expiry dates first. (Since iventory_list is ordered by expiry date, the stock in the top rows are expiring first and will be sold in an order, ascending in expiration date.)

                # A sale of a certain amount of a product may consists of different "Id's" of the product (due to different buy- and expiration-dates).
                # Each sale of an "Id" will be recorded separtely in the sold.csv:
                if sale_counter >= stock_quantity_in_row:
                    add_product_to_csv(
                        sold_csv_file,
                        inventory_product["Id"],
                        inventory_product["product_name"],
                        inventory_product["quantity"],
                        inventory_product["expiration_date"],
                        "no_buy_date_needed",
                        "no_buy_price_needed",
                        args.sales_price,
                    )
                    inventory_list.remove(
                        inventory_product
                    )  # this adjusted inventory_list will be written to the inventory_csv_file at the end of this sell-function in the final 'if...else' body, as more adjustments may be made to this inventory_list further in this sell-function.
                    sale_counter -= stock_quantity_in_row
                    if sale_counter == 0:
                        console.print(
                            f"You have succesfully sold {args.quantity} items of '{args.product_name}'.",
                            style="green",
                        )
                        break  # no need to loop further, as the amount of the sale has been reached
                else:  # ie: sale_counter < stock_quantity_in_row
                    # entering this "else"-body means there is a left-over in the sale_counter (as the amount of a sale certainly does not always have an incidental, exact match with a sum of buy-quantity-registrations).
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

    if in_stock == False:
        console.print(
            f"There is no registrated stock of this product '{args.product_name}'. First add stock using the 'buy' function of this programm",
            style="red",
        )
    else:
        write_csv_file(inventory_csv_file, inventory_list)
        if sale_counter > 0:
            # when the inventory_list is totally looped and there is still a remnant in the sale_counter: it means the amount entered in 'sell' exceeds the total amount available in the inventory. It will be handled with the message as followed:
            console.print(
                f"Only {stock_counter} items instead of {args.quantity} items of '{args.product_name}' are registered as 'sold', as there are only {stock_counter} items of '{args.product_name}' registered in inventory. \nFirst add the residu to the inventory using the 'buy' function. Re-entry in the 'sell' function in order to sell this residu.",
                style="red",
            )
