# Instructions for Use

## Starting the program

In Terminal, run

```
python3 client.py
```

This will connect to a pre-specified spreadsheet (see the README for instructions on how to change the default spreadsheet). 
After a successful connection, a menu will be displayed.

## Entering a New Receipt

Entering '1' at the menu will begin the receipt entry process. Information about the receipt will be asked in the following order:

- Date of purchase
- Store/location name
- Items purchased
- Tax amount
- Notes about purchase/visit

More information about each is provided below.

### Date of Purchase

Enter the date of purchase (the date you visited the location/store) as a forward-slash separated date. The format that the program accepts is MM/DD/YYYY.

Valid date formats:

```
12/25/2021
```

Invalid date formats:

```
12/25/21
2021/12/25
12-25-2021
12.25.2021
2021-12-25
2021.12.25
```

### Store/Location Name

Enter the name of the store/location you visited to make the purchase.

### Items Purchased

Enter the owners of the item as a comma-separated list

Valid item formats:

```
Bike // 39
Bike // 39.99 // me, bob, trish
Soda//0.99
Shoes // 19.1 // nate
```

Invalid item formats:

```
Bike 39
Bike $39
Bike / 39
Bike // $39
Bike 39 me, bob, trish
Bike // 39 // me + bob + trish
```

Make sure to enter any tips you gave, as tips will be considered an item as well.

### Tax Amount

Enter the tax as shown on the receipt, without the dollar sign ('$'). Pressing 'Enter' without specifying a tax value will assume tax is $0.00.

Valid tax formats:

```
19
19.
19.9
19.99
.99
```

Invalid tax formats:

```
$19.99
```

### Notes

Enter any notes about the visit, items purchased, or store here. Make sure to type the notes without pressing 'Enter' before you are finished,
as 'Enter' will indicate you are done typing notes.

## Sorting the Receipts

To sort by date, enter '2' at the menu.

To sort by total cost, enter '3' at the menu

## Displaying all Receipts

To display the receipts from the spreadsheet, enter '4' at the menu.

## Displaying Connection Info

The connection info is used to verify the name of the Google spreadsheet and worksheet that the program is connected to.
To display this info, enter '5' at the menu.

## Ending the Program

To end the program, enter 'Q' or 'q' at the menu. This will close the connection between the program and the spreadsheet.
