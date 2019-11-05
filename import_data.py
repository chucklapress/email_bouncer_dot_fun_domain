#!/usr/bin/env python3
import csv
import psycopg2
import time
import shutil

with open('/home/chucklapress/spam_table/test.csv') as in_file:
    with open('/home/chucklapress/spam_table/new_data.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if any (row):
                writer.writerow(row)


conn = psycopg2.connect("host=localhost dbname=myproject user=myprojectuser password=password")
cur = conn.cursor()
#UNCOMMENT BELOW TO SET INITIAL TABLE IN DATABASE
cur.execute("DROP TABLE IF EXISTS email_parser_raw")

table_create_command = """CREATE TABLE email_parser_raw (
    mail TEXT
);"""

#cur.execute(table_create_command)
with open('/home/chucklapress/spam_table/new_data.csv','r') as f:
    print("csv file open")
    reading = csv.reader(f)
    reader = csv.reader(f)
    for row in reader:
        print(row)
        cur.execute(
        "INSERT INTO email_parser_raw (mail) VALUES(%s)",
        row
        );

    conn.commit()
shutil.os.remove("/home/chucklapress/spam_table/test.csv")
shutil.os.remove("/home/chucklapress/spam_table/new_data.csv")
conn.close()
