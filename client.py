"""
Expense Tracker - client.py

Author: Zach Chin
Last modified: June 1, 2021

Usage: 
	python3 client.py [-d]

TODO:
	o Add ability to prevent duplicate entries?
	o Add insert row at proper location rather than needing to sort all at the end
	o Error trap when no items are entered
	o Prevent negative numbers
"""

from receipt import Receipt, Item
from item_console import ItemConsole
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
KEYFILE_NAME = "expense-tracker.json"
SPREADSHEET = "Expenses"	# specify which spreadsheet to open

class Client:
	def __init__(self, debug):
		# use creds to create a client to interact with the Google Drive API
		self.scope = SCOPE
		self.creds = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE_NAME, SCOPE)
		self.client = gspread.authorize(self.creds)

		# Find a workbook by name and open the first sheet
		print("Connecting to spreadsheet \"" + SPREADSHEET + "\"...")
		self.spreadsheet = self.client.open(SPREADSHEET)

		# Not debugging
		if debug == 0:
			self.worksheet = self.spreadsheet.sheet1
		# Debugging
		else:
			self.worksheet = self.spreadsheet.worksheet("Sheet2") # Test sheet
		print("Connected successfully to worksheet \"" + str(self.worksheet.title) + "\"!")

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
		console = ItemConsole(receipt)
		console.run()

	def get_tax(self, receipt):
		tax = input("Enter the tax amount (press enter to continue if no tax): ")
		while True:
			# If the user presses enter, assume tax is 0
			if tax == '': 
				tax = 0.0
			# Verify that the entered tax is a floating point number
			try:
				receipt.add_item(Item('Tax', float(tax)))
				break
			except ValueError:
				tax = input("The given tax is not a number! Enter the tax amount: ")

	def get_notes(self, receipt):
		notes = input("Add notes (hit enter to continue): ")
		receipt.set_notes(notes)

	def add_receipt(self):
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
				receipt.get_type(),								# type of receipt (PERSONAL or SHARED)
				receipt.get_notes()]							# notes
		
		print("Adding receipt...")

		# Append row of data to the worksheet
		self.worksheet.append_row(data, value_input_option='USER_ENTERED')
		print(receipt)
		print("Receipt added!")

	def sort_by_date(self):
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

		print("\nSorted!")

	def sort_by_cost(self):
		# Load all worksheet data into a dataframe
		df = pd.DataFrame(self.worksheet.get_all_records())

		# If the costs are strings, convert them to floating-point values
		if df.dtypes['Total'] == "object":
			df['Total'] = df['Total'].str.replace('$', '', regex=False)
			df['Total'] = df['Total'].str.replace(',', '', regex=False)
			df['Total'] = pd.to_numeric(df['Total'],errors='raise')

		# Sort the costs
		df = df.sort_values(by=['Total'], ascending=True)

		# Change the floats back to currency format
		df['Total'] = df['Total'].map("${:,.2f}".format)

		# Write the dataframe back to the worksheet
		self.worksheet.update([df.columns.values.tolist()] + df.values.tolist())

		print("\nSorted!")


	def print_receipts(self):
		# Load all worksheet data into a dataframe
		df = pd.DataFrame(self.worksheet.get_all_records())

		# Print receipts in dataframe
		print("\nReceipts: \n")
		print(df)

	def print_connection_info(self):
		print("\nConnection information:\n" +\
				"  Spreadsheet title: " + self.spreadsheet.title + "\n" +\
				"  Worksheet title: " + self.worksheet.title + "\n")

	def run(self):
		# Display menu continuously until user quits
		while True:
			print("\n***** Expense Tracker Menu *****\n" +\
				"  1. Enter a new receipt\n" +\
				"  2. Sort receipts by date\n" +\
				"  3. Sort receipts by cost\n" +\
				"  4. Print receipts\n" +\
				"  5. Print connection information\n" +\
				"  Q. Quit the program")
			menu_choice = input("Select an option by typing the number: ")
			if menu_choice == '1':
				self.add_receipt()
			elif menu_choice == '2':
				self.sort_by_date()
			elif menu_choice == '3':
				self.sort_by_cost()
			elif menu_choice == '4':
				self.print_receipts()
			elif menu_choice == '5':
				self.print_connection_info()
			elif menu_choice.lower() == 'q':
				break
			else:
				print("\nInvalid option!")

# Get command-line arguments
args = sys.argv
if len(args) == 1:
	debug = 0
elif len(args) > 1:
	arg1 = args[1].lower()
	if arg1 == "-d":
		debug = 1
	else:
		print("Usage: python3 client.py [debug]")
		exit()
else:
	print("Usage: python3 client.py [debug]")
	exit()


# Initialize client
client = Client(debug)
client.run()

