# covid_slot_check
A python script to check empty slots for vaccination for below 45 folks. Use cron to run it repeatedly at given interval.

# Requirement
You will require the following libraries for the script.
1. datetime
2. requests
3. argparse
4. simpleaudio 

# Setup
Once you have the script in your local machine, you need to run the script at regular interval.
You can use cron to do that.

For example, you can add the below line to your crontab to run the script every 5 minutes.
In your terminal, 
Do `crontab -e` in your terminal. Add the below line.
`*/5 * * * * python3 /path/to/python/script/check_cowin_status.py -p [pincodes seperated by space] -d [number_of_days] -a [age_to_check]`