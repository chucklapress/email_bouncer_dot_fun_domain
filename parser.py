#!/usr/bin/env python3

import os, sys
import email
import re
import mailparser
import datetime

def parser():
    path = "/home/chucklapress/Maildir/new"
    dirs = os.listdir( path )
    new_dir = '/home/chucklapress/Maildir/new/'
    handoff_dir = '/home/chucklapress/Maildir/tmp/'
    cur_dir = '/home/chucklapress/Maildir/cur/'
    parsed_file = open('/home/chucklapress/processed/mail_objects.csv','a')#modified to append to prevent overwrite

    for file in dirs:
        os.rename(new_dir + file , handoff_dir + file + '.1')
        print('**********************************',file=parsed_file)
        print (file , file=parsed_file)
        print('**********************************',file=parsed_file)

        mail = mailparser.parse_from_file(handoff_dir + file + '.1')
        mail_from = mail.from_[0][1]
        mail_to = [m[1] for m in mail.to]
        mail_subject = mail.subject
        mail_domain = mail_from.split('@')[1]
        headers = {
            'subject': mail_subject,
            'to': mail_to,
            'from': mail_from,
            'domain': mail_domain
        }
        print('_____________________________________________', file=parsed_file)
        print(headers, file=parsed_file)
        mail_spamassassin = mail.X_Spam_Status.replace("\n\t", " ")
        mail_spf_records = mail.Received_SPF.split(';')[0]
        spamassassin_results = {
            'spamassassin': mail_spamassassin,
            'SPF': mail_spf_records
        }
        print('_____________________________________________', file=parsed_file)
        print(spamassassin_results, file=parsed_file)
        time_parsed = datetime.datetime.now()
        print('parsed at: '+str(time_parsed), file=parsed_file)
        print('this indicates the script ran')

        os.rename(handoff_dir + file + '.1' , cur_dir + file + '.2')
        if cur_dir + file + '.2':
            pass
        else:
            os.rename(handoff_dir + file + '.1',  new_dir + file)


if __name__ == '__main__':
    parser()
