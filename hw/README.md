# MPCS51220

1. Open terminal, go to folder hw1 that has file hw1.py

2. Start my app (python3)
$ python3 hw1.py
This will run the program. 

3. Assumptions:
- The users will type the valid inputs (for example, can only cancel existing reservations, etc.). 
- Users type only the integer when being asked choosing the options.
- Client names are unique
- A reservation will allow booking 1 workshop or 1 machine
- Clients can only make reservations of the future date and time
- Clients will book time within in 30 minute blocks and always start on the hour or half hour.

4. What I have implemented:
- Implementing a json file to save data of every program call
- Validating working hours
- Make reservations for clients, including calculating total cost and down payment cost.
- Ensure that reservations don't violate any availability rules -- no more than 15 workshops at a time and the machine constraints listed above (see validations in reservation.py).
- Cancel reservations when requested by a client, and calculate the appropriate refund amount.
- Generate a report of the reservations for any given date range.
List the financial transactions for any given date range (past or future). This should account for cancellations.
- List the reservations for a given customer for a given date range.
- Every reservation has a unique serial number (using uuid).
- Users  can only reserve one special machine at a time, but their workshop reservation can overlap machine rentals.

5. My codes are so ugly sometimes I can't debug my own codes.

6. Examples:
Example input is put in "" (when typing in terminal you exclude the "". Hit enter for inputing)

* Make reservations
$ python3 hw1.py
$ Option: "1"
$ Enter client name: "Lilypad"
$ Option: "1" (reserve a workshop)
$ Enter time start reservation(YYYY/mm/dd-HH:MM):"2021/04/15-11:00"
$ Enter time end reservation(YYYY/mm/dd-HH:MM): "2021/04/15-11:30"
(Saved to reservation.json)

$ python3 hw1.py
$ Option: "1"
$ Enter client name: "MarshMallow"
$ Option: "2" (reserve a mini microvacs)
$ Enter time start reservation(YYYY/mm/dd-HH:MM):"2021/04/15-11:00"
$ Enter time end reservation(YYYY/mm/dd-HH:MM): "2021/04/15-11:30"
(Saved to reservation.json)

* Cancel reservations
$ python3 hw1.py
$ Option: "2"
$ Enter client name:"Lilypad"
$ Option: 1

* Generate reservation report
$ python3 hw1.py
$ Option: "3"
$ Start date(YYYY/mm/dd): "2021/04/15"
$ End date(YYYY/mm/dd): "2021/04/17"

* List financial transactions
$ python3 hw1.py
$ Option: "4"
$ Start date(YYYY/mm/dd): "2021/04/15"
$ End date(YYYY/mm/dd): "2021/04/17"

* List reservations for a customer
$ python3 hw1.py
$ Option: "5"
$ Enter client name:"Lilypad"
$ Start date(YYYY/mm/dd): "2021/04/15"
$ End date(YYYY/mm/dd): "2021/04/17"









