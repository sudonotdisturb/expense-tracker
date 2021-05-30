"""
Expense Tracker - client.py

Author: Zach Chin
Last modified: May 30, 2021

Usage: 
	python3 client.py

TODO:
	o Add ability to prevent duplicate entries?
	o Add insert row at proper location rather than needing to sort all at the end
	o Error trap when no items are entered
"""

from receipt import Receipt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class Client:
	def __init__(self):
		# use creds to create a client to interact with the Google Drive API
		self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
		self.creds = ServiceAccountCredentials.from_json_keyfile_name('expense-tracker.json', self.scope)
		self.client = gspread.authorize(self.creds)

		# Find a workbook by name and open the first sheet
		self.spreadsheet = self.client.open("Expenses")
		# self.worksheet = self.spreadsheet.sheet1
		self.worksheet = self.spreadsheet.worksheet("Sheet2") # Test sheet

	def get_date(self):
		return input("Enter the date of the receipt (MM/DD/YYYY): ")

	def is_valid_date(self, date):
		# Split date string
		date_parts = date.split('/')

		# Check that there are three parts to the date string
		if len(date_parts) == 3:
			if (int(date_parts[0]) >= 1 and int(date_parts[0]) <= 12 and # Check month is valid
				int(date_parts[1]) >= 1 and int(date_parts[1]) <= 31 and # Check day is valid
				int(date_parts[2]) >= 1000):							 # Check year is valid
				return True
		
		# If tests above fail
		print("Invalid date format!")
		return False

	def get_items(self, receipt):
		print("\nEnter your item name and cost (without $ sign) separated by a double slash (//)." +\
				"\nRead the README for complete help on entering items." +\
				"\nType \"done\" to quit.")
		while True:
			item = input("  New item> ").lower()
			if item == "done" or item == "quit" or item == "exit":
				break
			receipt.add_item(item)

	def get_tax(self, receipt):
		tax = input("Enter the tax amount (press enter to continue if no tax): ")
		while True:
			# If the user presses enter, assume tax is 0
			if tax == '': 
				tax = 0.0
				continue
			# Verify that the entered tax is a floating point number
			try:
				float(tax)
				break
			except ValueError:
				tax = input("The given tax is not a number! Enter the tax amount: ")
		receipt.add_item("Tax" + "//" + str(tax))

	def get_notes(self, receipt):
		notes = input("Add notes (hit enter to continue): ")
		receipt.set_notes(notes)

	def sort(self):
		# Load all worksheet data into a dataframe
		df = pd.DataFrame(self.worksheet.get_all_records())
		# test_worksheet = self.spreadsheet.add_worksheet(title="Test", rows="100", cols="5")

		# Get the dates in the dataframe as DateTime objects
		date_sr = pd.to_datetime(df['Date'])

		# Change the dates to be in YYYY/MM/DD format
		df['Date'] = date_sr.dt.strftime('%Y/%m/%d')

		# Sort the dates
		df = df.sort_values(by=['Date'], ascending=True)

		# Change the dates back to MM/DD/YYYY format
		df['Date'] = date_sr.dt.strftime('%m/%d/%Y')

		# Write the dataframe back to the worksheet
		self.worksheet.update([df.columns.values.tolist()] + df.values.tolist())

	def run(self):
		# Get the date for the receipt and verify it is valid
		date = self.get_date()
		while not self.is_valid_date(date):
			date = self.get_date()

		# Get store name
		store = input("Enter the store name: ")

		# Create receipt
		receipt = Receipt(date, store)

		# Get items on receipt
		self.get_items(receipt)

		# Get tax
		self.get_tax(receipt)

		# Get notes
		self.get_notes(receipt)

		# Put receipt data into dataframe
		data = [date, 											# date
				store, 											# location
				'$' + str(round(receipt.get_total_cost(), 2)), 	# total cost
				receipt.get_item_list(), 						# list of items bought
				receipt.get_notes()]							# notes
		
		# Append row of data to the worksheet
		self.worksheet.append_row(data, value_input_option='USER_ENTERED')
		print(receipt)
		print("Receipt added!")


# Initialize client
client = Client()

# Allow user to enter as many receipts as desired
while True:
	add_receipt = input("Add a new receipt? (y/n) ").lower()
	if add_receipt == 'n' or add_receipt == 'no':
		break
	elif add_receipt == 'y' or add_receipt == 'yes':
		client.run()
	else:
		print("Invalid choice! Please enter \'y\' or \'n\'.")

# Update the spreadsheet to be sorted by date
print("Sorting receipts...")
client.sort()
print("Done!")