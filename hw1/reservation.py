from datetime import date, datetime, time, timedelta
import math
import uuid
import json

POW_MAX =7

class Schedule(dict):
    #start hour
    start = None
    #end hour
    end = None
    # Working hours: 9 am - 6pm Mon - Fri
    # Working hours: 10am - 4 pm Sat
    def __init__(self, start: datetime, end: datetime):
        now = (datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=30))
        if start < now:
            start = now
        if start > now.replace(hour=0,minute=0)+ timedelta(days=30):
            # can not make a reservation on more than 30 days from now.
            return

        if start.minute<=30 and start.minute>0:
            print('1')
            start = start.replace(minute=30,second=0,microsecond=0)
        elif start.minute>30:
            print('2')
            start = start.replace(hour=start.hour+1,minute=0,second=0,microsecond=0)

        if start.weekday() == 6:
            print('3')
            start = (start + timedelta(days=1)).replace(hour=9, minute=0,second=0,microsecond=0)
        elif start.weekday() == 5:
            if start < start.replace(hour=10,minute=0,second=0,microsecond=0):
                print('4')
                start = start.replace(hour=10, minute=0, second=0, microsecond=0)
            else:
                print('41')
                if start >= start.replace(hour=16,minute=0,second=0,microsecond=0):
                    start = (start + timedelta(days=2)).replace(hour=9, minute=0,second=0,microsecond=0)
        else:
            print('5')
            if start < start.replace(hour=9, minute=0, second=0, microsecond=0):
                start = start.replace(hour=9, minute=0, second=0, microsecond=0)
            elif start>= start.replace(hour=18, minute=0, microsecond=0, second=0):
                print(f'5aa {start} {start.weekday()}')
                if start.weekday() == 4:
                    print('5ab')
                    start = (start+timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
                else:
                    start = (start+timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
                    print('5ac')


        if end.weekday() == 6:
            print('6')
            end = (end- timedelta(days=1)).replace(hour=16, minute=0,second=0,microsecond=0)
        elif end.weekday() == 5:
            if end > end.replace(hour=16, minute=0, microsecond=0, second=0):
                print('7')
                end = end.replace(hour=16,minute=0,second=0,microsecond=0)
            elif end < end.replace(hour=10, minute=0, microsecond=0, second=0):
                print('8')
                end = (end-timedelta(days=1)).replace(hour=18,minute=0,second=0,microsecond=0)
        elif end.weekday == 0:
            if end > end.replace(hour=18, minute=0, microsecond=0, second=0):
                print('9')
                end = end.replace(hour=18,minute=0,second=0,microsecond=0)
            elif end < end.replace(hour=9, minute=0, microsecond=0, second=0):
                print('10')
                end = (end-timedelta(days=2)).replace(hour=16,minute=0,second=0,microsecond=0)

        else:
            if end > end.replace(hour=18, minute=0, microsecond=0, second=0):
                print('11')
                end = end.replace(hour=18,minute=0,second=0,microsecond=0)
            elif end < end.replace(hour=9, minute=0, microsecond=0, second=0):
                print('12')
                end = (end-timedelta(days=1)).replace(hour=18,minute=0,second=0,microsecond=0)

        if start>= end:
            #invalid schedule
            return
        self.start = start
        self.end = end
        dict.__init__(self,__type__='schedule', start=start.strftime('%Y/%m/%d-%H:%M'),end=end.strftime('%Y/%m/%d-%H:%M'))


    def counte(self,end) -> timedelta:
        # Expect all start and end time have be bound to legit working hours
        a= self.start
        b= end
        total = timedelta()
        # full day rental
        while b>a.replace(hour=20):
            if a.weekday()==6:
                total += timedelta()
                a = (a+timedelta(days=1)).replace(hour=9, minute=0, microsecond=0, second=0)
            elif a.weekday() == 5:
                total += a.replace(hour=16,minute=0,second=0,microsecond=0) - a
                a = (a+timedelta(days=1)).replace(hour=9, minute=0, microsecond=0, second=0)
            elif a.weekday() ==4:
                total += a.replace(hour=18,minute=0,second=0,microsecond=0) - a
                a = (a+timedelta(days=1)).replace(hour=10, minute=0, microsecond=0, second=0)
            else:
                total += a.replace(hour=18,minute=0,second=0,microsecond=0) - a
                a = (a + timedelta(days=1)).replace(hour=9, minute=0, microsecond=0, second=0)
        # get remaining hours
        total += b-a
        return total
    def count(self) -> timedelta:
        # Expect all start and end time have be bound to legit working hours
        a= self.start
        b= self.end
        total = timedelta()
        # full day rental
        while b>a.replace(hour=20):
            if a.weekday()==6:
                total += timedelta()
                a = (a+timedelta(days=1)).replace(hour=9, minute=0, microsecond=0, second=0)
            elif a.weekday() == 5:
                total += a.replace(hour=16,minute=0,second=0,microsecond=0) - a
                a = (a+timedelta(days=1)).replace(hour=9, minute=0, microsecond=0, second=0)
            elif a.weekday() ==4:
                total += a.replace(hour=18,minute=0,second=0,microsecond=0) - a
                a = (a+timedelta(days=1)).replace(hour=10, minute=0, microsecond=0, second=0)
            else:
                total += a.replace(hour=18,minute=0,second=0,microsecond=0) - a
                a = (a + timedelta(days=1)).replace(hour=9, minute=0, microsecond=0, second=0)
        # get remaining hours
        total += b-a
        return total

    def __repr__(self):
        return f'[{self.start} to {self.end}]'

class Wshop(dict):
    def __init__(self, name='Workshop', qt=15, power=0, price=99, dp=0, unit=timedelta(hours=1)) -> None:
        self.name= name
        self.qt = qt
        self.power = power
        self.price = price
        self.dp = dp
        self.unit = unit
        dict.__init__(self, __type__='workshop',name=self.name,qt=self.qt,price=self.price,unit= self.unit.seconds,power=self.power,dp=self.dp)

    def valid(self,  client ,orders, schedule)-> bool:
        overlap = 0
        for order in orders:
            if isinstance(order.item , Wshop):
                if order.schedule.start > schedule.start:
                    if not (order.schedule.start >= schedule.end):
                        overlap +=1
                else:
                    if not (schedule.start >= order.schedule.end):
                        overlap += 1
        return overlap<self.qt

    def __repr__(self) -> str:
        return f'{self.name}'

class Harves(dict):
    def __init__(self, name='1.21 Gigawatt lightning harvester', qt=2, power=4, price=8800, dp=0.5, unit=timedelta(hours=1)) -> None:
        self.name= name
        self.qt = qt
        self.power = power
        self.price = price
        self.dp = dp
        self.unit = unit
        dict.__init__(self,__type__='harves',name=self.name,qt=self.qt,price=self.price,unit= self.unit.seconds,power=self.power,dp=self.dp)

    def valid(self, client, orders, schedule) -> bool:
        overlap = 0
        power = 0
        for order in orders:
            if not isinstance(order.item , Wshop):
                if order.schedule.start > schedule.start:
                    if not (order.schedule.start >= schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item, Harves):
                            overlap +=1
                        power += order.item.power
                else:
                    if not (schedule.start >= order.schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item , Harves):
                            overlap +=1
                        power += order.item.power

        return overlap<self.qt and power<= POW_MAX-self.power

    def __repr__(self) -> str:
        return f'{self.name}'
class Micro(dict):
    def __init__(self, name='Mini microvac', qt=2, power=1, price=2000, dp=0.5, unit=timedelta(hours=1)) -> None:
        self.name= name
        self.qt = qt
        self.power = power
        self.price = price
        self.dp = dp
        self.unit = unit
        dict.__init__(self,__type__='micro', name=self.name,qt=self.qt,price=self.price,unit= self.unit.seconds,power=self.power,dp=self.dp)
    def valid(self, client, orders, schedule) -> bool:
        overlap = 0
        power = 0
        for order in orders:
            if not isinstance(order.item , Wshop):
                if order.schedule.start > schedule.start:
                    if not (order.schedule.start >= schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item, Micro):
                            overlap +=1
                        power +=order.item.power


                else:
                    if not (schedule.start >= order.schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item , Micro):
                            overlap +=1
                        power +=order.item.power
        return overlap<self.qt and power<=POW_MAX-self.power

    def __repr__(self) -> str:
        return f'{self.name}'
class Extru(dict):
    def __init__(self, name='Polymer Extruder', qt=2, power=1, price=500, dp=0.5, unit=timedelta(hours=1)) -> None:
        self.name= name
        self.qt = qt
        self.power = power
        self.price = price
        self.dp = dp
        self.unit = unit
        dict.__init__(self, __type__='extru',name=self.name,qt=self.qt,price=self.price,unit= self.unit.seconds,power=self.power,dp=self.dp)
    def valid(self, client, orders, schedule) -> bool:
        overlap = 0
        power =0
        for order in orders:
            if not isinstance(order.item , Wshop):
                if order.schedule.start > schedule.start:
                    if not (order.schedule.start >= schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item , Extru):
                            overlap +=1
                        power +=order.item.power
                else:
                    if not (schedule.start >= order.schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item ,Extru):
                            overlap +=1
                        power +=order.item.power
        return overlap<self.qt and power<=POW_MAX-self.power

    def __repr__(self) -> str:
        return f'{self.name}'
class Crusher(dict):
    def __init__(self, name='High Velocity Crusher', qt=1, power=1, price=10000, dp=0.5, unit=timedelta(minutes=30)) -> None:
        self.name= name
        self.qt = qt
        self.power = power
        self.price = price
        self.dp = dp
        self.unit = unit
        dict.__init__(self, __type__='crusher',name=self.name,qt=self.qt,price=self.price,unit= self.unit.seconds,power=self.power,dp=self.dp)
    def valid(self, client, orders, schedule)-> bool:
        if schedule.end - schedule.start > timedelta(minutes=30):
            print('Client can not rent a high velocity crusher for more than 30 minutes')
            return False
        overlap = 0
        power = 0
        for order in orders:
            if not isinstance(order.item , Wshop):
                if order.schedule.start > schedule.start:
                    if not (order.schedule.start >= schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        power +=order.item.power
                else:

                    if not (schedule.start >= order.schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        power +=order.item.power
            if isinstance(order.item , Crusher):
                if order.schedule.start > schedule.start:
                    if not (order.schedule.start >= schedule.end+ timedelta(hours=6)):
                        overlap +=1
                else:
                    if not (schedule.start >= order.schedule.end+ timedelta(hours=6)):
                        overlap += 1
        return overlap<self.qt and power<= POW_MAX - self.power

    def __repr__(self) -> str:
        return f'{self.name}'
class Irrad(dict):
    def __init__(self, name='Irradiator', qt=2, power=1, price=2200, dp=0.5, unit=timedelta(hours=1)) -> None:
        self.name= name
        self.qt = qt
        self.power = power
        self.price = price
        self.dp = dp
        self.unit = unit
        dict.__init__(self,__type__='irrad', name=self.name,qt=self.qt,price=self.price,unit= self.unit.seconds,power=self.power,dp=self.dp)
    def valid(self, client, orders, schedule)->bool:
        overlap = 0
        power =0
        for order in orders:
            if not isinstance(order.item, Wshop):
                if order.schedule.start > schedule.start:
                    print('a')
                    if not (order.schedule.start >= schedule.end):
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item ,Irrad):
                            overlap +=1
                        power +=order.item.power
                else:
                    print('b')
                    if not (schedule.start >= order.schedule.end):
                        print('c')
                        # Client already rent a special machine at given time
                        if order.client == client:
                            return False
                        if isinstance(order.item ,Irrad):
                            overlap +=1
                        power +=order.item.power
        return overlap==0 and power<=POW_MAX-self.power
    def __repr__(self) -> str:
        return f'{self.name}'

class Order(dict):
    def __init__(self,id ,client:str, schedule:Schedule , item = None, cancl= False,crdate = datetime.now()) -> None:
        if id is None:
            self.id = uuid.uuid4().urn
        else:
            self.id = id
        self.schedule = schedule
        self.item = item
        self.client = client
        self.crdate = crdate
        self.cancl = cancl
        dict.__init__(self,__type__='order',id=self.id, schedule=schedule,item=item,client=client,crdate=self.crdate.strftime('%Y/%m/%d-%H:%M'),cancl=self.cancl)
        pass
    def tcost(self, e=None) -> int:
        #get total duration
        t= None
        if e is None:
            t = self.schedule.count()
        else:
            t = self.schedule.counte(e)
        return math.ceil(t / self.item.unit) * self.item.price * (1- self.disc())
    def disc(self)->float:
        if (self.crdate+ timedelta(days=14))< self.schedule.start:
            return 0.25
        return 0


    def dcost(self) -> int:
        return self.tcost() * self.item.dp
    def cancel(self) -> float:
        self.cancl = True
        dict.update(self,cancl=self.cancl)
        # get refund 
        if (datetime.now() + timedelta(days=2)) >= self.schedule.start:
            return self.dcost() * 0.5
        if (datetime.now() + timedelta(days=7)) >= self.schedule.start:
            return self.tcost()*0.75
        return self.tcost()



    def __repr__(self) -> str:
        return f'Order:[client: {self.client}, schedule: {self.schedule}, item:{self.item}, cancel:{self.cancl}]'
class App:
    orders : list
    def __init__(self, orders) -> None:
        self.orders = orders

    def make(self,client:str, s:Schedule, item):
        if self.valid(client, s, item):
            order = Order(id=uuid.uuid4().urn,client=client, schedule=s, item=item)
            self.orders.append(order)
            print(f'Make a reservation successed: {order}')
            print(f'Total cost: {order.tcost()}')
            print(f'Down payment cost: {order.dcost()}')

            # jsonStr = json.dumps(self.orders)
            # print(jsonStr)
            with open('reservation.json', 'w') as f:
                json.dump(self.orders,f)

        else:
            print(f'Can not make a reservation for order: [{client}, {s}, {item}]')


    def valid(self, client, s, item) -> bool:
        if s.start is None or s.end is None:
            return False
        orders = []
        for o in self.orders:
            if not o.cancl:
                orders.append(o)

        vail = item.valid(client,orders, s)
        overs= set()
        overe = set()
        startw = s.start.isocalendar()[1]
        endw = s.end.isocalendar()[1]
        for order in orders:
            if order.client == client:
                if order.schedule.start.isocalendar()[1] == startw:
                    overs.add(order.id)
                if order.schedule.end.isocalendar()[1] ==endw:
                    overs.add(order.id)

        overlap = max(len(overs), len(overe))
        return vail and overlap < 3

    def cancel(self, id: str):
        for i in range(len(self.orders)):
            if self.orders[i].id == id:
                refund = self.orders[i].cancel()
                print(f'Refund ${refund} for reservation: {self.orders[i]}')
                with open('reservation.json', 'w') as f:
                    json.dump(self.orders,f)

    def search(self, client: str)-> list:
        result = []
        for o in self.orders:
            if o.client == client:
                if not o.cancl:
                    result.append(o)
        return result
    def report(self,start, end)-> list:
        result = []
        # print(self.orders)
        for o in self.orders:
            print(o)
            if o.schedule.start>= start and o.schedule.start< end:
                result.append(o)
        return result
    def clientrp(self, client, start, end)-> list:
        orders = self.report(start, end)
        result = []
        for o in orders:
            if o.client == client:
                result.append(o)
        return result


