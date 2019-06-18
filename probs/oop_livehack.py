# Define the Item class here
class Item(object):
   def __init__(self, item_name, quantity):
       """
       item constructor

       :param string item_name: name of item
       :param int quantity: amount available to loan
       """
       self.__item_name = item_name
       self.__quantity = quantity

   def get_name(self):
       """
       return name of item

       :return string: name of item
       """
       return self.__item_name

   def get_quantity(self):
       """
       Return the quantity of the item available

       :return int: quantity of items
       """
       return self.__quantity

   def set_quantity(self, quantity):
       """
       Update the quantity of the item to new_qty

       :param int quantity: new quantity of item
       :return: None
       """
       self.__quantity = quantity

   def __str__(self):
       """
       String representation of the item in the form 'Item Name, qty'

       :return string: item name and quantity separated by a comma and space
       """
       return ", ".join((self.__item_name, str(self.__quantity)))


class Library(object):
   def __init__(self):
       """
       Library constructor
       """
       self.__item_collection = []

   def add_new_item(self, item_name, qty):
       """
       Add a new item to the library item collection

       :param str item_name: name of the item to add
       :param int qty: amount of the item to add
       :return: None
       """
       # ADD YOUR CODE HERE
       self.__item_collection.append(Item(item_name, qty))

   def __get_item(self, item_name):
       """
       Retrieve an item from the item collection

       :param str item_name: the name of the item to retrieve
       :return: Item
       """
       for item in self.__item_collection:
           if item.get_name() == item_name:
               return item

   def loan_item(self, item_name):
       """
       Loan an item from the item collection

       :param str item_name: name of the item to loan
       :return: None
       """
       loan = self.__get_item(item_name)
       if loan.get_quantity() > 0:
           loan.set_quantity(loan.get_quantity() - 1)
       else:
           print(loan.get_name() + " is unavailable.")

   def return_item(self, item_name):
       """
       Return an item (that was on loan) to the item collection. Adds one to the quantity of the specified

       :param item_name: the name of the item to return
       :return: None
       """
       # ADD YOUR CODE HERE
       loan = self.__get_item(item_name)
       loan.set_quantity(loan.get_quantity() + 1)

   def print_inventory(self):
       """
       Print out all items along with their inventory

       :return: None
       """
       # ADD YOUR CODE HERE
       max_length = 0
       for item in self.__item_collection:
           length = len(item.get_name())
           if length > max_length:
               max_length = length
       formatting = "".join(("{0: <", str(max_length), "}"))
       print("----------\nINVENTORY:\n----------")
       for item in self.__item_collection:
           # print(item) # looks like hot garbage
           print(" : ".join((formatting.format(item.get_name()), str(item.get_quantity()))))

# -------- Main Program ----------------------

# Code the following ...
if __name__ == "__main__":


    # create an instance of the library
    lib_1 = Library()
    # Add the the following items to the library, with specified quantities :
    #   hdmi cable - 3
    #   usb charger - 5
    #   power adapter - 2
    lib_1.add_new_item("HDMI CABLE", 3)
    lib_1.add_new_item("USB CHARGER", 5)
    lib_1.add_new_item("POWER ADAPTER", 2)

    # print the inventory
    lib_1.print_inventory()

    # loan a usb charger
    # loan an hdmi cable
    lib_1.loan_item("USB CHARGER")
    lib_1.loan_item("HDMI CABLE")

    # print the inventory
    lib_1.print_inventory()

    # return a usb charger
    lib_1.return_item("USB CHARGER")
    # print the inventory
    lib_1.print_inventory()

