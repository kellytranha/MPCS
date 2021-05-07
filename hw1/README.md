## MPCS 51220 1 Applied Software Engineering
## A-01 - Assignment: Write some ugly code
## Yaroslav Vergun

## Assumptions
The user should enter dates that are consistent with the requirements below.

Normal operating hours are 9am to 6pm every weekday and 10 am to 4pm on Saturdays. 
Sundays are closed for maintenance.
Reservations are made in 30 minute blocks and always start on the hour or half hour.
The minimum reservation time is 30 minutes. 

The down payment is paid at the time the reservation is made.
The rest of the total payment is paid all at once at the start of the first reserved activity.
Down payment refunds are paid at the time a cancellation is made.

An example of a reservation is:
```
Serial Number: 1
Client: Mike Jones
Canceled: 2021-04-05 13:50
Made time: 2021-04-05 13:47
Start time: 2021-06-15 09:00
Components: 
     workshop 2021-06-15 09:00, 2021-06-15 18:00
     microvac 2021-06-15 12:00, 2021-06-15 13:00
```

Made time represents when the reservation was made. 
Canceled is either None, or the time that a cancellation was made.
Start time is the first starting time of any of the components.


There is no correctness/error checking in the code.
If something is misspelled or parsing fails, the code will error.

## How to run
The application is run via one of the following commands
```shell
python3 app.py add
python3 app.py cancel
python3 app.py report
python3 app.py customer
python3 app.py transactions
```

The command line arguments `add/cancel/report/customer/transactions` allow the user to add a reservation, cancel a reservation, generate a report of (non-canceled) reservations for a given date range, list the reservations for a customer for a given date range, and to list the financial transactions for a given date range (handling cancellations).

After running one of the above commands, further instructions are displayed. 

Canceling a reservation requires a serial number.
This can be found by looking at a report of the reservations or by looking at a customer report (or by looking in `records.txt`).

Note that dates must be entered in exactly the format `YYYY-MM-DD HH:MM`, i.e. `2021-04-04 13:30`.
The user has to be very careful in entering dates in the correct format and also to spell everything correctly. 

Reservation records are saved in the file `records.txt`.
The application reads the records, sometimes modifes or appends records and writes back to the file.

Sample reservation records are included in `records_sample.txt`.
Those can just be pasted into `records.txt` to have examples or something non-empty to work with.

The application ran and worked on the remote linux cs machines.

## Simplifications / Omissions
There are no special instructions for recurring reservations. 
The user can enter the information for a recurring reservation one item at a time in the same way a non-recurring reservation is entered. If that's entered normally, it will count as one reservation.

There is no restriction on the number of days in advance that a reservation can be made. 
There is nothing preventing a reservation of being made in the past. 

 
## Bugs
Have not run into bugs.

## Ugliness
The code is hard to read with no explanations and very short variable names.
Code is repeated a bunch. Everything is in one file. 
