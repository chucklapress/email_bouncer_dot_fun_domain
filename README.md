# Email-bouncer project
This application contains python scripts and a django project that work in unison
Ideally it is deployed on a Linux server with a Postfix mail server as its mail handler
## Installation
This application requires a number of working pieces links are provided for good sources to get the required parts.
## Mail Server
mail server: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-on-ubuntu-18-04
## Django, Postgres and NGINX
django postgres and nginx: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04
## SpamAssassin
Spamassassin: https://hostadvice.com/how-to/how-to-secure-postfix-with-spamassassin-on-an-ubuntu-18-04-vps-or-dedicated-server/ and https://www.digitalocean.com/community/tutorials/how-to-install-and-setup-spamassassin-on-ubuntu-12-04
## Unbound
Information on Unbound: https://launchpad.net/ubuntu/bionic/+source/unbound and python3-unbound and libunbound-dev
## Making System packages work inside python virtualenv
special care should be made to allow access to Unbound by following
Fixing the virtualenv global issue---
If you need to change this option after creating a virtual environment, you can add (to turn off) or remove (to turn on) the file no-global-site-packages.txt from lib/python3.7/ or equivalent in the environments directory.
Other considerations Celery is dependent on Redis being available on the running instance

## Usage
The deployed Django application has a functional button that will open the users mail client to send a test email to your mail client
You will need to start the Celery worker with the assigned task send_email and utilize one of the two methods of either another_trigger.py or new_approach.py which operate as listeners for incoming mail at Maildir/new directory and kick off parser_new.py and data_import.py which are required to parse the raw headers, save the fields as a database object as well as a CSV file which Django's built in send_mail function uses to return the results.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
-- HTML email is currently a hot mess so be fore-warned to either heavily modify it or use the plain text virgin

## Improvements
Once the email server is up and running it is strongly suggested that the following are added to utilize the full functionality of the application
Python-SPF, OpenDKIM, OpenDMARC these libraries when connected to the Postfix mail server will provide the needed raw header verifications with SpamAssassin to provide a full testing suite against the senders email_parser
links are included for implementing these additions:
SPF and OpenDKIM: https://www.linuxbabe.com/mail-server/setting-up-dkim-and-spf
OpenDMARC: https://www.linuxbabe.com/mail-server/opendmarc-postfix-ubuntu

## License
[MIT](https://choosealicense.com/licenses/mit/)
