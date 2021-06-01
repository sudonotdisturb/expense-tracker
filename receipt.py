"""
receipt.py

Author: Zach Chin
Last modified: June 1, 2021

"""
class Receipt:
	def __init__(self, date, store, receipt_type = "PERSONAL"):
		self.date = date
		self.store = store
		self.items = []
		self.type = receipt_type
		self.notes = ''

	def add_item(self, item):
		self.items.append(item)

	def pop_item(self):
		self.items.pop()

	def set_type(self, receipt_type):
		self.type = receipt_type

	def set_notes(self, notes):
		self.notes = notes

	def get_items(self):
		return self.items

	def get_item_list(self):
		if self.type == "PERSONAL":
			item_list = [i.get_name() + " (" + str(i.get_cost()) + ")" for i in self.items]
			return ', '.join(item_list)
		else:
			item_list = [i.get_name() + " (" + str(i.get_cost()) + ") - paid by " + i.get_owner_string() for i in self.items]
			return "\n".join(item_list)

	def get_total_cost(self):
		item_costs = [i.get_cost() for i in self.items]
		return sum(item_costs)

	def get_type(self):
		return self.type

	def get_notes(self):
		return self.notes

	def __str__(self):
		# Get string of items purchased
		item_string = ""
		for i in self.items:
			item_string += "- {0:}: ${1:.2f} (paid by {2})\n".format(i.get_name(), i.get_cost(), i.get_owner_string())

		return "\n************** {0} Receipt ****************\n".format(self.store) +\
				"Date: {0}\n".format(self.date) +\
				"Items bought:\n{0}\n".format(item_string) +\
				"Total cost: ${0:.2f}\n".format(round(self.get_total_cost(), 2)) +\
				"Notes: {0}".format(self.notes) +\
				"\n**********************************************\n"


class Item:
	# Constructor
	def __init__(self, name, cost, owners = None):
		self.name = name
		self.cost = cost
		if owners == None:
			self.owners = ['me']
		else:
			self.owners = owners

	def get_name(self): 
		return self.name

	def get_cost(self): 
		return self.cost

	def get_owners(self):
		return self.owners

	def get_num_owners(self):
		return len(self.owners)

	def get_owner_string(self):
		return ', '.join(self.owners)