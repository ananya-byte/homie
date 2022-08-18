import csv
filename = "/home/pi/Desktop/homie/permissions.csv"

def hosts_list():
    fields = []
    rows = []
    hosts = []
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        numfield = len(fields)
        for row in csvreader:
            rows.append(row)
            if row!=[] and row[2]=='YES' and row[3]=='NO':
                hosts.append(int(row[0]))
    return hosts

def guests_list():
    fields = []
    rows = []
    guests = []
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        numfield = len(fields)
        for row in csvreader:
            rows.append(row)
            if row!=[] and row[2]=='NO' and row[3]=='YES':
                guests.append(int(row[0]))
    return guests

def appendhost(chat_id,name):
    element = ["","","",""]
    element[0]=str(chat_id)
    element[1]=name
    element[2]='YES'
    element[3]='NO'
    with open(filename, 'a+', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            continue
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(element)


def appendguest(chat_id,name):
    element = ["","","",""]
    element[0]=str(chat_id)
    element[1]=name
    element[2]='NO'
    element[3]='YES'
    with open(filename, 'a+', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            continue
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(element)

def checkhost(chat_id):
    hosts = hosts_list()
    for x in hosts:
        if chat_id==x:
            return True
    return False

def checkguest(chat_id):
    guests = guests_list()
    for x in guests:
        if chat_id==x:
            return True
    return False
