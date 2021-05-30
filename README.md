# Expense Tracker

Expense Tracker is a tool that enables the easy and quick entry of receipts into a Google spreadsheet for personal finances. For my purposes, the data is sent to a spreadsheet in my personal Google Drive.

Usage:

```python3 client.py```

In order to enable this tool for your own Google spreadsheet purposes, follow the steps outlined in [this blog](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/). After downloading the key in JSON format, name the JSON file "expense-tracker.json" and place it in this project directory. If you would like to use a different name for your JSON file, find the line:

```
self.creds = ServiceAccountCredentials.from_json_keyfile_name('expense-tracker.json', self.scope)
```

And replace `expense-tracker.json` with your JSON filename.

*Note*: The Google Cloud Platform has changed slightly since the writing of that blog post, so some exact steps may be inaccurate. The basic idea is to create a service account for the application, and generate a new key to download in JSON format.

To change the spreadsheet being edited, find the line:

```
self.sheet = self.client.open("Expenses").sheet1
```

Change the string "Expenses" to the name of your Google spreadsheet.
