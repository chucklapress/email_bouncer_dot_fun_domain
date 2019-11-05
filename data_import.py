#!/usr/bin/env python3
import csv
import psycopg2
import time
import shutil
#code can be uncommented to create table for dmarc_check in django application
#start = time.perf_counter()
#time.sleep(1) # do work
#elapsed = time.perf_counter() - start
#print(f'Time {elapsed:0.4}')
conn = psycopg2.connect("host=localhost dbname=myproject user=myprojectuser password=password")
cur = conn.cursor()

#cur.execute("DROP TABLE IF EXISTS email_parser_dmarc_check")

#table_create_command = """CREATE TABLE email_parser_dmarc_check (
    #id SERIAL,
    #address VARCHAR(100),
    #domain VARCHAR(30),
    #subject VARCHAR(100),
    #the_dmarc_record VARCHAR(360),
    #time_parsed VARCHAR(100),
    #return_from VARCHAR(100)

#);"""

#cur.execute(table_create_command)
with open('/home/chucklapress/new_processed/newest.csv', 'r') as f:
    print("csv file open")
    reading = csv.reader(f)
    reader = csv.reader(f)
    for row in reader:
        print(row)
        cur.execute(
        "INSERT INTO email_parser_dmarc_check (address, domain, subject, the_dmarc_record, time_parsed, return_from) VALUES(%s, %s, %s, %s, %s, %s)",
        row
        );

    conn.commit()
shutil.os.remove("/home/chucklapress/new_processed/newest.csv")
conn.close()


#This script takes the CSV file created by the parser function and adds a line of data to the database
#added remove new_processed/newest.csv after data upload to prevent rewriting database
