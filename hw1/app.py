#!/usr/bin/env python3

import sys
from datetime import datetime, timedelta
from collections import namedtuple
from dataclasses import dataclass
from typing import Any

CHRG = {
  'workshop': 99.0,
  'microvac': 2000.0,
  'irradiator': 2200.0,
  'extruder': 500.0,
  'crusher': 20000.0,
  'harvester': 8800.0,
}

@dataclass
class rsvtn:
    srln: int
    clien: str
    cancl: Any
    made: Any
    strt: Any
    lst: list

def r_pnt(res):
  print(f"Serial Number: {res.srln}")
  print(f"Client: {res.clien}")
  if res.cancl:
    print(f"Canceled: {res.cancl.isoformat(sep=' ', timespec='minutes')}")
  else:
    print(f"Canceled: {res.cancl}")
  print(f"Made time: {res.made.isoformat(sep=' ', timespec='minutes')}")
  print(f"Start time: {res.strt.isoformat(sep=' ', timespec='minutes')}")
  print(f"Components: ")
  for x in res.lst:
    print("    ", x.kind, x.strt.isoformat(sep=' ', timespec='minutes') + ",", x.end.isoformat(sep=' ', timespec='minutes'))
  print()


rtup = namedtuple('rtup', ['kind', 'strt', 'end'])

#  d = datetime.fromisoformat('2011-11-04 09:30')

def itsc(a, b):
  return ((a.strt < b.end) and (b.strt < a.end))


def vld(recs, new):
  nws = [x for x in new.lst if x.kind == 'workshop']
  nmvs = [x for x in new.lst if x.kind == 'microvac']
  nirs = [x for x in new.lst if x.kind == 'irradiator']
  nexs = [x for x in new.lst if x.kind == 'extruder']
  ncrs = [x for x in new.lst if x.kind == 'crusher']
  nhvs = [x for x in new.lst if x.kind == 'harvester']

  wsps = []
  for r in recs:
    if not r.cancl:
      r_ws = [x for x in r.lst if x.kind == 'workshop']
      wsps = wsps + r_ws

  big = nws + wsps
  for el in nws:
    ins = [1 for x in big if itsc(el, x)]
    if len(ins) > 15:
      return "more than 15 workshops"

  mvs = []
  for r in recs:
    if not r.cancl:
      r_mvs = [x for x in r.lst if x.kind == 'microvac']
      mvs = mvs + r_mvs

  big = nmvs + mvs
  for el in nmvs:
    ins = [1 for x in big if itsc(el, x)]
    if len(ins) > 2:
      return "more than 2 microvacs"

  irs = []
  for r in recs:
    if not r.cancl:
      r_irs = [x for x in r.lst if x.kind == 'irradiator']
      irs = irs + r_irs

  big = nirs + irs
  for el in nirs:
    ins_1 = 0
    ins_2 = 0
    ins_3 = 0
    el_cd = rtup(el.kind, el.end, el.end + timedelta(hours=1))
    for x in big:
      if itsc(el, x):
        ins_1 += 1
      x_new = rtup(x.kind, x.end, x.end + timedelta(hours=1))
      if itsc(el, x_new):
        ins_2 += 1
      if itsc(el_cd, x):
        ins_3 += 1
    if (ins_1 > 1) or (ins_2 > 1) or (ins_3 > 1):
      return "failed irradiator constraint"

  exs = []
  for r in recs:
    if not r.cancl:
      r_exs = [x for x in r.lst if x.kind == 'extruder']
      exs = exs + r_exs

  big = nexs + exs
  for el in nexs:
    ins = [1 for x in big if itsc(el, x)]
    if len(ins) > 2:
      return "more than 2 extruders"

  crs = []
  for r in recs:
    if not r.cancl:
      r_crs = [x for x in r.lst if x.kind == 'crusher']
      crs = crs + r_crs

  big = ncrs + crs
  for el in ncrs:
    el_nw = rtup(el.kind, el.strt, el.end + timedelta(hours=6))
    ins = 0
    for x in big:
      x_new = rtup(x.kind, x.strt, x.end + timedelta(hours=6))
      if itsc(el_nw, x_new):
        ins += 1
    if ins > 1:
      return "failed crusher constraint"
  
  hvs = []
  for r in recs:
    if not r.cancl:
      r_hvs = [x for x in r.lst if x.kind == 'harvester']
      hvs = hvs + r_hvs

  big = nhvs + hvs
  for el in nhvs:
    ins = [1 for x in big if itsc(el, x)]
    if (len(ins)>1):
      return "harvester constraint failed"

  oths = nmvs + mvs + nirs + irs + nexs + exs + ncrs + crs
  for el in (nhvs + hvs):
    ins2 = [1 for x in oths if itsc(el, x)]
    if len(ins2)>3:
      return "harvester constraint failed"

  spcl = []
  for r in recs:
    if (not r.cancl) and (r.clien == new.clien):
      r_spl = [x for x in r.lst if x.kind in ['microvac', 'irradiator', 'extruder', 'crusher', 'harvester']]
      spcl = spcl + r_spl

  alem = spcl + nmvs + nirs + nexs + ncrs + nhvs
  for el in alem:
    ins = [1 for x in alem if itsc(el, x)]
    if len(ins) > 1:
      return "allowed only 1 special machine at a time"

  rrs = []
  for r in recs:
    if (not r.cancl) and (r.clien == new.clien):
      rrs = rrs + r.lst
  rrs = rrs + new.lst
  weks = dict()
  for r in rrs:
    z = r.strt.isocalendar()
    if (z[0], z[1]) not in weks:
      weks[(z[0], z[1])] = set([z[2]])
    else:
      weks[(z[0], z[1])].add(z[2])
    if len(weks[(z[0], z[1])]) > 3:
      return "can only make reservations for 3 different days in a week"

  return "ok"


if __name__ == "__main__":
  cmd = sys.argv[1]
  
  with open("records.txt", mode='r') as in_f:
    recs = []
    for line in in_f:
      stuff = line.rstrip('\n').split('; ')
      srln = int(stuff[0])
      clien = stuff[1]
      if stuff[2] == 'None':
        cancl = None
      else:
        cancl = datetime.fromisoformat(stuff[2])
      made = datetime.fromisoformat(stuff[3])
      strt = datetime.fromisoformat(stuff[4])
      lst = []
      for x in stuff[5:]:
        words = x.split(' ')
        lst.append(rtup(words[0], datetime.fromisoformat(words[1] + " " + words[2]), datetime.fromisoformat(words[3] + " " + words[4])))
      recs.append(rsvtn(srln, clien, cancl, made, strt, lst))

  # for x in recs:
  #   r_pnt(x)
    

  if cmd == 'add':
    srln = len(recs) + 1
    clien = input("Enter client name: ")
    cancl = None
    lst = []
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Enter desired reservations one item at a time")
    print("Enter DONE to finish")
    print("a reservation item has to be entered in EXACTLY the format below")
    print("Thing StartTime EndTime")
    print("Thing can only be one of: workshop, microvac, irradiator, extruder, crusher, harvester")
    print("StartTime and EndTime have to have the format YYYY-MM-DD HH:MM")
    print("Examples:")
    print("workshop 2021-06-17 09:30 2021-06-17 17:00")
    print("harvester 2021-05-01 11:00 2021-05-01 12:00")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    inpu = input("Enter a reservation item, or type DONE\n") 
    while inpu != "DONE":
      words = inpu.split(' ')
      lst.append(rtup(words[0], datetime.fromisoformat(words[1] + " " + words[2]), datetime.fromisoformat(words[3] + " " + words[4])))
      inpu = input("\nEnter a reservation item, or type DONE\n")

    if lst:
      strt = lst[0].strt
      for tu in lst:
        if tu.strt < strt:
          strt = tu.strt

    
    made = datetime.fromisoformat(datetime.now().isoformat(sep=' ', timespec='minutes'))
    new = rsvtn(srln, clien, cancl, made, strt, lst)

    # this does the obvious
    wat = vld(recs, new)

    if wat == 'ok':
      recs.append(new)

      scal = 1.0
      delt = new.strt - new.made
      if delt.days >= 14:
        scal = 0.75

      w_cst = 0
      m_cst = 0
      for x in new.lst:
        if x.kind == 'workshop':
          w_cst += CHRG['workshop']*(((x.end - x.strt).seconds)/3600.0)
        else:
          m_cst += CHRG[x.kind]*(((x.end - x.strt).seconds)/3600.0)
      
      print("\nTotal cost: ", scal*(w_cst + m_cst))
      print("Down payment: ", 0.5*scal*m_cst)

    else:
      print("\nFAILED due to:")
      print(wat)

  
  elif cmd == 'cancel':
    csn = input("Enter the serial number of the reservation to cancel: ")
    for x in recs:
      if x.srln == int(csn):
        x.cancl = datetime.fromisoformat(datetime.now().isoformat(sep=' ', timespec='minutes'))

        scal = 1.0
        delt_m = x.strt - x.made
        if delt_m.days >= 14:
          scal = 0.75

        m_cst = 0
        for z in x.lst:
          if z.kind != 'workshop':
            m_cst += CHRG[z.kind]*(((z.end - z.strt).seconds)/3600.0)
        
        delt_c = x.strt - x.cancl
        if delt_c.days >= 7:
          print("\nRefund on down payment: ", 0.75*0.5*scal*m_cst)
        elif delt_c.days >= 2:
          print("\nRefund on down payment: ", 0.5*0.5*scal*m_cst)
        else:
          print("\nRefund on down payment:  0.0")

        break


  elif cmd == 'report':
    print("Enter date range in exactly the format below")
    print("YYYY-MM-DD HH:MM       (example: 2021-05-01 09:30)")
    print("First enter the start date, and then the end date\n")
    dst = datetime.fromisoformat(input("Enter start date: "))
    den = datetime.fromisoformat(input("Enter end date:   "))
    rang = rtup('range', dst, den)

    print("\n\nREPORT\n")
    for x in recs:
      if (not x.cancl) and any(itsc(rang, el) for el in x.lst):
        r_pnt(x)

  elif cmd == 'customer':
    print("Enter customer name and then the date range")
    print("Enter date range in exactly the format below")
    print("YYYY-MM-DD HH:MM       (example: 2021-05-01 09:30)")
    print("After entering the name, enter the start date, and then the end date\n")
    name = input("Enter customer name: ")
    dst = datetime.fromisoformat(input("Enter start date: "))
    den = datetime.fromisoformat(input("Enter end date:   "))
    rang = rtup('range', dst, den)

    print("\n\nCLIENT REPORT\n")
    for x in recs:
      if (x.clien == name) and any(itsc(rang, el) for el in x.lst):
        r_pnt(x)

  elif cmd == 'transactions':
    print("Enter date range in exactly the format below")
    print("YYYY-MM-DD HH:MM       (example: 2021-05-01 09:30)")
    print("First enter the start date, and then the end date\n")
    dst = datetime.fromisoformat(input("Enter start date: "))
    den = datetime.fromisoformat(input("Enter end date:   "))

    print("\n\nTRANSACTIONS\n")
    for r in recs:

      scal = 1.0
      delt = r.strt - r.made
      if delt.days >= 14:
        scal = 0.75

      w_cst = 0
      m_cst = 0
      for x in r.lst:
        if x.kind == 'workshop':
          w_cst += CHRG['workshop']*(((x.end - x.strt).seconds)/3600.0)
        else:
          m_cst += CHRG[x.kind]*(((x.end - x.strt).seconds)/3600.0)
      
      tot_c = scal*(w_cst + m_cst)
      dwn_p = 0.5*scal*m_cst
      rfnd = 0.0

      if r.cancl:
        delt_c = r.strt - r.cancl
        if delt_c.days >= 7:
          rfnd = 0.75*dwn_p
        elif delt_c.days >= 2:
          rfnd = 0.5*dwn_p

      if (dst <= r.made) and (r.made <= den):
        if dwn_p > 0:
          print(f"Serial number: {r.srln}")
          print(f"Date: {r.made}")
          print(f"{r.clien} paid {dwn_p}\n")

      if (not r.cancl) and (dst <= r.strt) and (r.strt <= den):
        print(f"Serial number: {r.srln}")
        print(f"Date: {r.strt}")
        print(f"{r.clien} paid {tot_c - dwn_p}\n")

      if r.cancl and (rfnd > 0) and (dst <= r.cancl) and (r.cancl <= den):
        print(f"Serial number: {r.srln}")
        print(f"Date: {r.cancl}")
        print(f"{r.clien} was refunded {rfnd}\n")


  # print("\ndid stuff\n")
  # print()
  # for x in recs:
  #   r_pnt(x)
    
  if cmd in ['add', 'cancel']:
    with open("records.txt", mode='w') as in_f:
      for x in recs:
        in_f.write(str(x.srln) + "; ")
        in_f.write(x.clien + "; ")
        if x.cancl:
          in_f.write(x.cancl.isoformat(sep=' ', timespec='minutes') + "; ")
        else:
          in_f.write("None; ")
        in_f.write(x.made.isoformat(sep=' ', timespec='minutes') + "; ")
        in_f.write(x.strt.isoformat(sep=' ', timespec='minutes') + "; ")
        tups = []
        for tup in x.lst:
          tups.append(tup.kind + " " + tup.strt.isoformat(sep=' ', timespec='minutes') + " " + tup.end.isoformat(sep=' ', timespec='minutes'))
        in_f.write('; '.join(tups) + "\n")

