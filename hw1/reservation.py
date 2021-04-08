import uuid
from datetime import datetime,timedelta,date,time

class Machine:
    schedules = []
    id = None
    price = None
    name = None
    downpay = None
    def __init__(self, price: int, name: str, downpay:bool):
        id = uuid.uuid4()
        self.price = price
        self.name = name
        self.downpay = downpay
        
        
    # def add_schedule(self,schedule):
    #     if self.validate_schedule(schedule):
    #         self.schedules.append(schedule)
        
    # def validate_schedule(self,schedule)-> bool:
    #     for d in schedule.dates:
    #         for s in self.schedules:
    #             if d in s.dates:
    #                 a_start  = datetime.combine(date.min,schedule.start) - datetime.min
    #                 a_end = datetime.combine(date.min,schedule.end) - datetime.min
    #                 c = datetime.combine(date.min,self.cooldown) - datetime.min
    #                 b_start = datetime.combine(date.min,s.start) - datetime.min
    #                 b_end = datetime.combine(date.min,s.end) - datetime.min + c
    #                 if (a_start> b_start && a_start<b_end) || (a_end>b_start && a_end<b_end):
    #                     return False
    #     return True
                    

    def __repr__(self):
        return f'Machine:[name:{self.name}, price:{self.price}]'
        
class Wshop:
    def __init__(self, price: int, name: str, downpay:bool):
        self.id = uuid.uuid4()
        self.price = price
        self.name = name
        self.downpay = downpay
        

class Equipment():
    def __init__(self, num, client, cost, down):
        self.sn = num # unique serial number
        self.client = client
        self.cost = cost
        self.down = down


class Order():
    def __init__(self,client, resers):
        self.id = uuid.uuid4()
        self.client = client
        self.resers = resers
    
    def cost(self)->int:
        result =0
        for r in self.resers:
            result += r.price
        return result
    # cost down payment
    def costdp(self)->int:
        result =0
        for r in self.resers:
            if r.
            result += r.price
        return result
    def __repr__(self):
        return f'Client:[name:{self.client.name}, reservations:{self.resers}]'


class Client():
    def __init__(self, name):
        self.name = name # assume client names are unique
    def __repr__(self):
        return f'Client:[name:{self.name}]'

class Schedule:
    #start hour
    start:datetime.time
    #end hour
    end:datetime.time
    #rent date 
    dates= []
    def __init__(self, start, end, dates):
        self.start = start
        self.end = end
        self.dates = dates
    def __repr__(self):
        return f'Schedule:[start:{self.start}, end:{self.end}, dates:{self.dates}]'
class App:
    orders: list
    clients : list
    items = [
        Machine(99,'Workshop',False),
        Machine(2000,'mini microvacs',True),
        Machine(2200,'irradiators',True),
        Machine(500,'polymer extruder',True),
        Machine(5000,'high velocity crusher',True),
        Machine(8800,'1.21 gigawatt lightning harvester',True),
    ]
  
    

    def __init__(self):
        self.clients = []
        self.orders =[]
        pass
    def make(self):
        # ask for client information
        # check if client in database
        # ask item
        # check avail
        # ask workshop
        # check avail
        # ask schedule
        # check avail
        # print cost
        name = input('Client name:')
        client = None
        for c in self.clients:
            if name == c.name:
                client = c
                break
        if not client:
            client = Client(name)
            self.clients.append(client)
        resers = {}
        while True:
            item = self.get_item_request()
            if not item:
                break
            if item.downpay:
                # check in list special machine reservations
                tmp  = False
                for i in resers:
                    if i.downpay:
                        tmp = True 
                        break
                if tmp:
                    print('You can only reserve one special machine at a time.')
                else:
                    item_schedule = self.get_item_schedule()
                    resers[item] = item_schedule
                    print(f'Added {item.name} to list reservation')
                    #self.reserve(item, item_schedule)
                    
            else:
                if item in resers:
                    print('You can only reserve one workshop at a time.')
                else:
                    item_schedule = self.get_item_schedule()
                    resers[item] = item_schedule
                    print(f'Added {item.name} to list reservation')
        
        if resers:
            order = Order(client=client,resers=resers)
            print('---------------------------')
            self.orders.append(order)

            print(f'Make reservation : {order}')
            print(f'Cost :  {order.cost()}')
        else:
            print('No reservations was make.')
        



    def reserve(self, item, schedule)-> Machine:

        item_schedule = self.get_item_schedule()
        # validate schedule
        # available resource 
        # get overlap date first

        badge ={}
        for d in item_schedule.dates:
            for order in self.orders:
                for resource in order.resers:
                    schedule = order.resers[resource]
                    for sd in schedule.dates:
                        if d == sd:
                            badge[schedule] = resource
        



        # can only make reservations for three different days in a given week


        resers[item] = item_schedule
        print(f'Added {item.name} to list reservation')


    def get_item_schedule(self):
        print('---------------------------')
        print(f'Enter schedule:')
        start = input('Start hour(HH:MM): ')
        start_t = datetime.strptime(start,'%H:%M').time()
        end = input('End hour(HH:MM): ')
        end_t = datetime.strptime(end,'%H:%M').time()
        dates =  []
        done = False
        while not done:
            d = input('Enter date reservation(YYYY/mm/dd):')
            d_d =  datetime.strptime(d,'%Y/%m/%d').date()
            dates.append(d)
            add_more = input('Recurring schedule (y/N)?: ')
            done = add_more != 'y'
        return Schedule(start, end, dates)

        
        
    def get_item_request(self):
        print('---------------------------')
        done = False
        while not done:
            # ask machines, each client can only borrow 1 machine
            print('List of resources in falicity:')
            for i in range(len(self.items)):
                print(f'{i+1}: {self.items[i].name}')
            print(f'{len(self.items)+1}: Cancel?')
            item = input(f'Choose requested item[1-{len(self.items)}]:')
            if item.isnumeric():
                item = int(item)
                if item == len(self.items)+1:
                    return None
                if item  in range(len(self.items)):
                    done = True
        return self.items[item-1]


    def cancel(self):
        pass
    def generat(self):
        pass
    def list_fin(self):
        pass
    def list_rev(self):
        pass

        