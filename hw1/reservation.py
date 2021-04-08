MINI_MICROVACS = 2
IRRADIATORS = 2
POLYMER_EXTRUDERS = 2
VELOCITY_CRUSHER = 1
LIGHTNING_HARVESTER = 1

WORKSHOP_PH = 99
MINI_MICROVAC_PH = 2000
IRRADIATOR_PH = 2200
POLYMER_EXTRUDE_PH = 500
VELOCITY_CRUSHER_PH = 10000
LIGHTNING_HARVESTER = 8800

class equipment():
    def __init__(self, num, client, cost, down):
        self.sn = num # unique serial number
        self.client = client
        self.cost = cost
        self.down = down


class reservation():
    def __init__(self, num, client, cost, down):
        self.sn = num # unique serial number
        self.client = client
        self.cost = cost
        self.down = down

class client():
    def __init__(self, name, client_id):
        self.name = name # unique serial number
        self.id = client_id
       