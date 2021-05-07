from datetime import datetime
import os

import reservation as res
import json

# object decoder
def decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == 'schedule':
            start = datetime.strptime(obj['start'], '%Y/%m/%d-%H:%M')
            end = datetime.strptime(obj['end'], '%Y/%m/%d-%H:%M')
            return res.Schedule(start, end)
        elif obj['__type__'] == 'order':
            crdate = datetime.strptime(obj['crdate'],'%Y/%m/%d-%H:%M')
            return res.Order(id=obj['id'],client=obj['client'],schedule=obj['schedule'],item=obj['item'],crdate=crdate,cancl=obj['cancl'])
        elif obj['__type__'] == 'workshop':
            return res.Wshop()
        elif obj['__type__'] == 'harves':
            return res.Harves()
        elif obj['__type__'] == 'extru':
            return res.Extru()
        elif obj['__type__'] == 'crusher':
            return res.Crusher()
        elif obj['__type__'] == 'irrad':
            return res.Irrad()
        elif obj['__type__'] =='micro':
            return res.Micro()
    else:
        return obj

# make reservations
def make_re(app:res.App):

    client = input('Enter client name: ')

    print('Make a reservation')
    print('=================')
    print('Choose one of resource below:')
    print('For example, if you want to make a reservation for Workshop, type 1 and hit enter')
    print('1- Workshop')
    print('2- Mini Microvacs')
    print('3- Irradiator')
    print('4- Polymer Extruder')
    print('5- High Velocity Crusher')
    print('6- 1.21 Gigawatt lightning harvester')
    print('7- Cancel?')

    option = input('Option: ')

    item = None
    if option == '1':
        item = res.Wshop()
    elif option == '2':
        item = res.Micro()
    elif option == '3':
        item = res.Irrad()
    elif option == '4':
        item = res.Extru()
    elif option == '5':
        item = res.Crusher()
    elif option == '6':
        item = res.Harves()
    elif option == '7':
        print('Cancelled make reservation!!')
        return

    start = input('Enter time start reservation(YYYY/mm/dd-HH:MM): ')
    end = input('Enter time end reservation(YYYY/mm/dd-HH:MM): ')

    s = res.Schedule(start=datetime.strptime(start, '%Y/%m/%d-%H:%M'), end=datetime.strptime(end, '%Y/%m/%d-%H:%M'))
    app.make_re(client,s,item)

# cancel reservations
def c_re(app: res.App):
    print('Cancel a reservation')
    print('=====================')
    client = input('Enter client name:')
    orders = app.search(client)
    if orders:
        print('Choose a reservation to cancel:')
        for o in range(len(orders)):
            print(f'{o+1}- {orders[o]}')
        index = input('Option: ')
        if index.isnumeric():
            i = int(index)
            if i > 0 and i <= len(orders):
                app.cancel(orders[i-1].id)
                print(f'Cancel a reservation successed: {orders[i-1]}')
        else:
            print('Cancel request is invalid!')
    else:
        print(f'Client {client} have no reservations')

# generate reservation report
def report(app: res.App):
    print('Reservation report')
    print('=========================')
    print('Enter date range')
    start = input('Start date(YYYY/mm/dd): ')
    end = input('End date(YYYY/mm/dd): ')
    orders = app.report(start=datetime.strptime(start, '%Y/%m/%d'), end=datetime.strptime(end, '%Y/%m/%d'))
    if orders:
        print('======================================================================================')
        print(f'                         Report   [{start} to {end}]                                            ')
        print('======================================================================================')
        print('Schedule             | client     | item     | create_date | cancelled | total cost  | down payment cost')
        for o in orders:
            print(f'{o.schedule}    | {o.client} | {o.item} | {o.crdate}  | {o.cancl} | {o.tcost()} | {o.dcost()}')

    else:
        print(f'No reservation on given date range: {start} - {end}')

# list financial transactions
def finrp(app: res.App):
    print('Financial Transactions Report')
    print('==========================')
    print('Enter date range')
    start = input('Start date(YYYY/mm/dd): ')
    end = input('End date(YYYY/mm/dd): ')
    startd = datetime.strptime(start, '%Y/%m/%d')
    endd= datetime.strptime(end, '%Y/%m/%d')
    orders = app.report(start=startd, end=endd)
    total = 0
    if orders:
        print('======================================================================================')
        print(f'                         Report   [{start} to {end}]                                            ')
        print('======================================================================================')
        print('Schedule             | client     | item     | create_date | cancelled | total cost  | down payment cost')
        for o in orders:
            print(f'{o.schedule}    | {o.client} | {o.item} | {o.crdate}  | {o.cancl} | {o.tcost(endd)} | {o.dcost()}')
            total +=o.tcost(endd)
            total += o.dcost()
        print(f'Total Revenue: {total}')
    else:
        print(f'No reservation on given date range: {start} - {end}')

# list reservations by client
def clntrp(app:res.App):
    print('Reservation report for client')
    print('=========================')
    print('Enter date range')
    client = input("Client name:")
    start = input('Start date(YYYY/mm/dd): ')
    end = input('End date(YYYY/mm/dd): ')
    orders = app.clntrp(client,start=datetime.strptime(start, '%Y/%m/%d'), end=datetime.strptime(end, '%Y/%m/%d'))
    if orders:
        print('======================================================================================')
        print(f' Client Report: {client}   [{start} to {end}]                                            ')
        print('======================================================================================')
        print('Schedule             | item     | create_date | cancelled | total cost  | down payment cost')
        for o in orders:
            print(f'{o.schedule}    | {o.item} | {o.crdate}  | {o.cancl} | {o.tcost()} | {o.dcost()}')

    else:
        print(f'No reservation on given date range: {start} - {end}')

if __name__ == '__main__':
    print('MPCS, Inc. - Laboratory Coworking Space Provider Management Application')
    print('=======================================================================')
    print('Choose one of the options:')
    print('For example, if you want to make a reservation, type 1 and hit enter')
    print('1- Make reservations')
    print('2- Cancel reservations')
    print('3- Generate reservation report')
    print('4- List financial transactions')
    print('5- List reservations for a customer')

    option = input("Option: ")
    data = []
    tmp = os.path.isfile('reservation.json')
    if tmp:
        with open('reservation.json') as json_file:
            data=json.load(json_file,object_hook=decoder)
    app = res.App(data)

    if option == '1':
        make_re(app)

    elif option == '2':
        c_re(app)

    elif option == '3':
        report(app)
    
    elif option == '4':
        finrp(app)
        
    # assume users choose 1-5
    else:
        clntrp(app)
