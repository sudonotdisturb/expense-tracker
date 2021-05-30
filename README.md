# Expense Tracker

Expense Tracker is a tool that enables the easy and quick entry of receipts into a Google spreadsheet for personal finances. For my purpose, the data is sent to a spreadsheet in my personal Google Drive.

Usage:

`python3 client.py`

In order to enable this tool for your own Google spreadsheet purposes, follow the steps outlined in [this blog](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/).

*Note*: The Google Cloud Platform has changed slightly since the writing of that blog post, so some exact steps may be inaccurate. The basic idea is to create a service account for the application, and generate a new key to download in JSON format.
