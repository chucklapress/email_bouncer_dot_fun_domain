#http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.core.mail import send_mail
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import unbound
from unbound import ub_ctx, ub_strerror, RR_TYPE_TXT
from unbound import ub_ctx,RR_TYPE_A,RR_CLASS_IN
import psycopg2
import time
import subprocess
app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# This will ultimately send the return results back to the email-bouncer tester
@app.task()
def send_email():
    from django.core.mail import send_mail
    from email_parser.models import dmarc_check
    path_to_watch = "/home/chucklapress/new_processed"
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
      time.sleep (2)
      after = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in after if not f in before]
      removed = [f for f in before if not f in after]
      if added:
          print( "Added: ", ", ".join (added))
          time.sleep(4)
          list = dmarc_check.objects.last()
          subject = list.subject
          from_email = list.return_from
          to = list.address
          domain = list.domain
          #spam_assassin = mail.X_Spam_Status.replace(",", ",\n")
          #dkim_signature = mail.DKIM_Signature.replace(";", ",\n")
          ctx = ub_ctx()
          ctx.set_option("module-config:","iterator")
          ctx.resolvconf("/etc/resolv.conf")
          status, result = ctx.resolve( domain, RR_TYPE_A, RR_CLASS_IN)
          if status == 0 and result.havedata:
              List = result.data.address_list
              results = " ".join(str(x) for x in List)
              #this line below will error out if email parsed is coming from localhost but that will never happen in production
              #Also this is only makeshift use of unbound to generate reverse dns look up a defined library will be utilized to define these
              status, result = ctx.resolve(unbound.reverse(results) + ".in-addr.arpa.", unbound.RR_TYPE_PTR, unbound.RR_CLASS_IN)
              if status == 0 and result.havedata:
                  NL = result.data.domain_list
                  reverse = " ".join(str(x) for x in NL)
              elif status != 0:
                  print( "Resolve error:", unbound.ub_strerror(status))
          other = subprocess.check_output(['dig',domain,'+short','TXT'])
          records = (other.decode('UTF-8','ignore'))
          body = '\n \n EMAIL-BOUNCER SCAN RESULTS\nHere are the results of our scan your DMARC record is: ,'+ list.the_dmarc_record + '\n thank you for using the DMARCIAN email-bouncer\n Results of a TXT search of your DNS resulted in:  '+ records + '\n Your IP was recorded as: '+ results+ 'and the reverse lookupon the IP  was: '+ reverse +'\n\Thank you for using the tool' #n--SpamAssassin Results--'+'\n \n' + spam_assassin+ '\n \n**How to interpret spamassassin results**\nThe first line is simply YES or NO to the fact that the email is spam\nthe next indicates a score based on lots of characteristics of the mail and they are scored any score below 5 indicates passing\nThe remaining keys are things that affected the score the complete key reference is here: https://spamassassin.apache.org/old/tests_3_3_x.html\n \n--DKIM Signature--' +'\n \n'+ dkim_signature + '\n \n**How to interpret dkim signature results**\nv= indicates version, a= indicates algorithm used to generate the signature, c= is the canonicalization algorithm\nd= indicates the domain, t= is the DKIM signature timestamp, bh= is the computed hash of the message body\nh= is a list of headers that will be used in the signing algorithm, b= is the hash data of the headers listed in the h= tag\nIf you would like to utilize the dmarcian phishing scorecard: https://www.phishingscorecard.com''\nYoull be asked to provide the DKIM key for your mail, this can be found in your results as s= the code following the = is the key\n \nThank you for using our tool, let us know how we can help you secure your email.\n \nContact us to help out support@dmarcian.com'
          send_mail(subject, body, from_email, [to], fail_silently=False)
          print('Email was sent')
      if removed: print( "Removed: ", ", ".join (removed))
      before = after
#This runs the system parser function which moves and parser the files in Maildir and places the results in processed
# Now it adds the functionality of storing processed/newest into postgres table
@app.task()
def run_parser_new():
    os.system("/home/chucklapress/./parser_new.py")
    print('parser_new program ran')
    time.sleep(2)
    os.system("/home/chucklapress/./data_import.py")
    print('successful sent to django database')

#removed refactored tasks after code refactoring on July 12
@app.task()
def send_html_email():
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from email_parser.models import dmarc_check
    list = dmarc_check.objects.last()
    subject = list.subject
    html_message = render_to_string('message.html', {'context': 'values'})
    plain_message = strip_tags(html_message)
    from_email = list.return_from
    to = list.address
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    print('html email sent')
#task that will be syncd to the email parse function I see it needing to be an html template with dynamic context for providing the results and returning them
