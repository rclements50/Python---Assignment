import matplotlib.pyplot as plt

record_list = []  # Creates the list for records to be inserted into


#  List created outside functions to give global scope

def read_file():
    infile = open("RECORD_DATA.txt", 'r')
    for row in infile:
        if not row.startswith("#"):
            row = row.rstrip("\n").split(', ')  # Strips the \n from items and splits by commas.
            record_list.append(row)  # Appends to record_list
    infile.close()


def main():
    # Displays the Main Menu.
    option = 0
    print("-------------------------------Menu----------------------------------")
    print("Summary Report      (1)\t\t\t\tSearch Prices Above Threshold  (2)")
    print("Genre Report        (3)\t\t\t\tAdd New Record                 (4)")
    print("Availability Query  (5)\t\t\t\tGenre Chart                    (6)")
    print("\t\t\t\t\t\tExit Program (7)")
    print("---------------------------------------------------------------------")
    # Asks the user for their option input.
    try:
        option = int(input("What would you like to do? : "))
    except ValueError:
        print("Error - Must be a number from 1 - 7")
        main()
    # Checks what they selected and calls functions based on what they choose.
    if option == 1:
        summary()
    elif option == 2:
        price_search()
    elif option == 3:
        genre_report()
    elif option == 4:
        add_record()
    elif option == 5:
        stock_search()
    elif option == 6:
        chart()
    elif option == 7:
        print("\t\t\t\tExiting Program")
        print("\t\t\t\tHave a nice day!")
        quit()
    else:
        print("Error - Must be a number from 1 - 7")
        main()


def summary():  # Menu Option Number One
    print("------------------------------Summary--------------------------------")
    total = 0
    value = 0.00
    for record in record_list:
        print(', '.join(record))  # Adds a comma between each list item
        total += 1
        value = value + float(record[6]) * int(record[5])  # Accumulator adds up total price of stock
    # Requires a key press to return to menu, used to slow the pace of the program down.
    print("---------------------------------------------------------------------")
    print("\nTotal Records: ", total, sep='')
    print("Total Price: £", format(value, '.2f'), sep='')  # Prints price accumulator
    print("\n---------------------------------------------------------------------")
    input("\nPress any key to return to menu: ")
    main()


def price_search():  # Menu Option Number Two
    items = 0
    print("-------------------------------Price_Check--------------------------------")
    try:
        price = float(input("Enter your price Threshold: £"))
    except ValueError:  # Checks if price is valid before continuing
        print("Error - Must be a valid price value")
        price_search()  # If not, calls the function again, allowing user to retry.
    if price < 0:
        print("Error - Must be a valid price value")
        price_search()
    for record in record_list:
        if price < float(record[6]):
            items += 1
            print(', '.join(record))
    if items == 0:
        print("No items above your price threshold")
    else:
        print("\nNumber of items above your threshold:", items)
        print("\n---------------------------------------------------------------------")
    input("Press any key to return to menu: ")
    main()


def genre_report():  # Menu Option Number Three
    print("-------------------------------Report--------------------------------")
    print("Genre\tAmount\n")
    genre = genre_adder()  # Calls the genre adder function and adds the dictionary to the genre dictionary
    for key, value in genre.items():  # Prints the dictionary keys and values beside them
        print(key, ': ', value)
    print("\n---------------------------------------------------------------------")
    input("Press any key to return to menu: ")
    main()  # Returns to the main menu


def genre_adder():
    genre = {}  # Creates empty dictionary names genre
    for record in record_list:
        if record[2] in genre:  # If the genre in each record is already in the dictionary, adds 1 to value.
            genre[record[2]] = int(genre[record[2]]) + 1
        else:
            genre[record[2]] = 1  # If genre is not in dictionary yet as key, assigns value as 1.
    return genre  # Returns the genre dictionary


def add_record():  # Menu Option Number Four
    string_builder = []
    value = input("Enter artists: ")  # Asks for Artists name input
    add_data(string_builder, value)  # Calls the addData function and sends it both the string_builder list plus the
    value = input("Enter Title: ")  # acquired data
    add_data(string_builder, value)
    value = input("Enter Genre: ")
    add_data(string_builder, value)
    value = input("Play Length: ")
    add_data(string_builder, value)
    value = input("Condition: ")
    add_data(string_builder, value)
    try:
        value = int(input("Stock: "))
    except ValueError:
        print("Error - Stock must be a whole, positive number")
        add_record()
    if value < 0:
        print("Error - Stock must be a whole, positive number")
        add_record()
    add_data(string_builder, str(value))
    try:
        value = float(input("Cost: £"))
    except ValueError:
        print("Error - Cost must be an appropriate price to two decimal places")
        #  https://stackoverflow.com/questions/23307209/checking-if-input-is-a-float-and-has-exactly-2-numbers-after-the-decimal-point
        #  Finds out if value added has at least one or two decimal places
    if len(str(value).rsplit('.')[-1]) == 1 or len(str(value).rsplit('.')[-1]) == 2:
        add_data(string_builder, str(value))
    else:
        print("Error - Cost must be an appropriate price to two decimal places")
        add_record()
    # Appends the newly formed record onto the record list
    record_list.append(string_builder)
    # Calls the summary function to display the new whole record list
    print("\nAdding New Record...")
    input("Press any key to see new record summary: ")
    summary()


def add_data(string_builder, value):
    # Finds the length of the value and uses it to determine how it shall be placed in the list
    index = len(str(value))
    # Converts value to string to find length. Useful for the quantity and cost data
    start = 0
    string_builder.append(value[start:index])
    print(string_builder)


def stock_search():  # Menu Option Number Five
    print("-------------------------------Record_Search--------------------------------")
    search = input("What title would you like to search for? ")
    found = False
    for record in record_list:
        if search in record[1]:  # Searches the title for the search input
            print("\nTitle: '", record[1], "' has been found!", sep='')
            found = True  # Sets value to true
            if int(record[5]) > 0:
                print("In Stock\nCopies:", record[5])
                print("\n---------------------------------------------------------------------")
            else:
                print("Out of Stock:", record[1])
                print("\n---------------------------------------------------------------------")
            print("\nWould you like to change the stock levels?\nIncrease(1)\nDecrease(2)\nExit to Main Menu(3)\n")
            try:
                stock_option = int(input("Use numbers 1 - 3 to decide: "))
            except ValueError:
                print("Must be a number 1 - 3")
                stock_search()
            if stock_option == 1:  # Mini menu allowing user to decide what they want to do next.
                increase(record)
            elif stock_option == 2:
                decrease(record)
            elif stock_option == 3:
                main()
    if not found:  # If value is still false, prints out the below message
        print("\nNo title found\n")
        stock_search()
    else:
        print("Returning to menu")


def increase(record):
    try:
        amount = int(input("How much would you like to increase stock by ? "))
    except ValueError:  # Checks to see if input is appropriate data type
        print("Error, Must be a whole positive number more than 0.")
        increase(record)
    if amount <= 0:
        print("Error, Must be a whole positive number more than 0.")
        increase(record)
    amount = amount + int(record[5])  # Adds the original stock value to the amount
    record[5] = str(amount)  # Assigns amount to the stock position in the list after converting to string
    print(', '.join(record))  # Prints the update record
    input("Press any key to return to menu: ")
    main()


def decrease(record):
    if int(record[5]) == 5:  # Checks to see if stock is already at 0
        print("Error, stock already at 0")
        stock_search()
    try:
        amount = int(input("How much would you like to decrease stock by ? "))
    except ValueError:  # Checks if it's appropriate data type and values
        print("Error - Must be a whole, positive number")
        decrease(record)
    if amount <= 0:
        print("Error - Must be a whole, positive number")
        decrease(record)
    if amount > int(record[5]):
        print("Error, not enough stock for transaction")
        decrease(record)  # Checks is stock is less than amount wished to decrease by
    amount = int(record[5]) - amount
    if amount == 0:
        print("Title now out of stock")
    record[5] = str(amount)  # Concerts new amount to string and assigns to list stock position
    print(', '.join(record))
    input("Press any key to return to menu: ")
    main()


def chart():  # Menu Option Number Six
    genre = genre_adder()  # Calls the genre_adder and receives the genre dictionary
    plt.bar(range(len(genre)), list(genre.values()))  # Uses dict values for bars
    plt.xticks(range(len(genre)), list(genre.keys()))  # Uses dict keys for bar labels
    plt.show()  # Sets the bar chart to show
    main()


# Calls the read_file function first to read in the data to a list from the text file and process it
read_file()
# Then Calls the main function which acts as our main menu
main()
