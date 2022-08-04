# cabin_scraping

Cabin scraping is a personal project, scraping data from realityidnes.cz with the pre-selected criteria of distance up to 2 hours and price below 4,000,000 CZK.

The code has been uploaded to AWS Lightsail, respectively to Ubuntu server and is running every morning at 8.00 hours, triggered by Crontab.

Further project notes:
Connecting to Lightsail service from AWS, create an account on AWS, Lightsail service —> [Connect Lightsail AWS](https://towardsdatascience.com/automate-python-scripts-with-aws-lightsail-b8dfdd5b0a2f)

create a static IP, download SSH key into the SSH folder, set it up

there might be an error —>  TERMINAL SSH KEYS: [WARNING: UNPROTECTED PRIVATE KEY FILE](https://www.howtogeek.com/168119/fixing-warning-unprotected-private-key-file-on-linux/)

authorize via terminal the ssh key

ssh -i ~/.ssh/AWS_Ubuntu.pem -T [ubuntu@3.73.147.133](mailto:ubuntu@3.73.147.133)

Project:

create a folder

pip freeze > requirements.text

upload the code on github with requirements.txt

git clone httsp:

**in terminal** 

sudo apt install python3-pip

`pip install -r requirements.txt`


Resources:
Automated web scraping: [https://towardsdatascience.com/automated-web-scraping-python-cron-e6bedf4c39eb](https://towardsdatascience.com/automated-web-scraping-python-cron-e6bedf4c39eb) 
TERMINAL SSH KEYS: [WARNING: UNPROTECTED PRIVATE KEY FILE](https://www.howtogeek.com/168119/fixing-warning-unprotected-private-key-file-on-linux/)
Crontab Guru: https://crontab.guru/
