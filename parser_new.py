#!/usr/bin/env python3
import os, sys
import email
import re
import time
import subprocess
import mailparser
import unbound
from unbound import ub_ctx, ub_strerror,RR_TYPE_TXT

path = "/home/chucklapress/Maildir/new"
dirs = os.listdir( path )
new_dir = '/home/chucklapress/Maildir/new/'
handoff_dir = '/home/chucklapress/Maildir/tmp/'
cur_dir = '/home/chucklapress/Maildir/cur/'
parsed_file = open('/home/chucklapress/new_processed/newest.csv','a')
other_test = open('/home/chucklapress/spam_table/test.csv', 'a')
for file in dirs:
    os.rename(new_dir + file , handoff_dir + file + '.1')
    mail = mailparser.parse_from_file(handoff_dir + file + '.1')

    plain_text = mail.text_plain
    subject = mail.subject
    date_sent = mail.date
    other_to = mail.to
    real_to = str(other_to)
    here_to =  ''.join(real_to)
    now_to = re.search(r'[\w\.-]+@[\w\.-]+', here_to)
    final_to = now_to.group(0)
    where_from = mail.from_
    source = str(where_from)
    match = re.search(r'[\w\.-]+@[\w\.-]+', source)
    address = match.group(0)
    domain = address.split('@')[1]
    spam_assassin = mail.X_Spam_Status.replace(",", ",\n")
    dkim_signature = mail.DKIM_Signature.replace(";", ",\n")
    print('this indicates the parse script ran')
    ctx = unbound.ub_ctx()
    ctx.resolvconf("/etc/resolv.conf")
    status, result = ctx.resolve("_dmarc."+str(domain), rrtype=RR_TYPE_TXT)
    if status == 0 and result.havedata:
        list1 = (result.data.data)
        str1 =  b''.join(list1)
        #print("Resuling data:" + str1.decode('utf-8', errors='ignore'))
        the_dmarc_record = str1.decode('utf-8', errors='ignore')
        print('dmarc passes')
        print(address+','+domain+','+subject.replace(",", " ")+','+the_dmarc_record.replace(","," ")+','+str(date_sent)+','+final_to, file=parsed_file)
        print(spam_assassin, file=other_test)
        print(dkim_signature,file=other_test)
    elif status != 0:
        print("Resolve error:", unbound.ub_strerror(status))
    else:
        print(address+','+domain+','+subject.replace(",", " ")+','+'No DMARC record found ,'+str(date_sent)+','+final_to, file=parsed_file)
        print(spam_assassin, file=other_test)
        print(dkim_signature, file=other_test)
    os.rename(handoff_dir + file + '.1' , cur_dir + file + '.2')
    if cur_dir + file + '.2':
        pass
    else:
        os.rename(handoff_dir + file + '.1',  new_dir + file)



# This script creates the CSV file to load the postgres table to return the data via the django email client
# re-written to utilize the dmarc_check and previous logic, makes more sense to import the data as a CSV instead of all unworkable text
# Added .replace(",", " ") to escape written commas in the subject line which breaks the CSV
