"""
receipt.py

Author: Zach Chin
Last modified: May 29, 2021

"""
class Receipt:
	def __init__(self, date, store):
		self.date = date
		self.store = store
		self.item_names = []
		self.item_costs = []
		self.notes = ''

	def add_item(self, item):
		# Verify that there is a '//' between the item name and cost
		try:
			name, cost = item.split('//')
			name = name.strip()
			cost = cost.strip()

			# Verify that cost is a number
			try:
				self.item_costs.append(float(cost))
				self.item_names.append(name)
			except ValueError:
				print("The given cost is not a number!")
		except ValueError:
			print("Put the separator \'//\' between the item name and cost!")

	def set_notes(self, notes):
		self.notes = notes

	def get_item_list(self):
		item_list = [self.item_names[i] + " (" + str(self.item_costs[i]) + ")" for i in range(len(self.item_names))]
		return ", ".join(item_list)

	def get_total_cost(self):
		return sum(self.item_costs)

	def get_notes(self):
		return self.notes

	def __str__(self):
		# Get string of items purchased
		item_string = ""
		for i in range(len(self.item_names)):
			item_string += "- {0:}: ${1:.2f}\n".format(self.item_names[i], self.item_costs[i])

		return "************** {0} Receipt ****************\n".format(self.store) +\
				"Date: " + self.date + "\n" +\
				"Items bought:\n" + item_string +\
				"******************************************"