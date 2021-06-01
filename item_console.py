"""
item_console.py

Author: Zach Chin
Last modified: June 1, 2021

"""

from receipt import Receipt, Item

class ItemConsole:
    def __init__(self, receipt):
        self.receipt = receipt

    def run(self):
        while True:
            item = input("  New item (${0:.2f})> ".format(self.receipt.get_total_cost()))
            cmd = item.lower()
            # Exiting item console
            if cmd == "done" or cmd == "quit" or cmd == "exit":
                break	
            # Undo the last item input
            elif cmd == "undo":
                try:
                    self.receipt.pop_item()
                except:
                    print("Cannot undo any further!")
            elif cmd == "":
                continue
            # If not a command, then assume input is an item
            else:
				# Verify that there is a '//' between the item name and cost
                try:
					# Get the name and cost
                    attributes = item.split('//')
                    name = attributes[0].strip()
                    cost = attributes[1].strip()

                    # Verify that cost is a number
                    try:
                        # If there are owners specified, get owners
                        if len(attributes) > 2:
                            owners = [owner.strip() for owner in attributes[2].strip().split(',')]
                            self.receipt.set_type("SHARED")
                            self.receipt.add_item(Item(name, float(cost), owners))
                        else:
                            self.receipt.add_item(Item(name, float(cost)))
                    except ValueError:
                        print("The given cost is not a number!")
                except:
                    print("Put the separator \'//\' between the item name and cost!")