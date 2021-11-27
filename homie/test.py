import csv

fields = ['ChatID','Name','Host','Guest']

rows= [['<chat-id>','<chat-name>','YES','NO']]

filename = "permissions.csv"

with open(filename,'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
    print("done.")
