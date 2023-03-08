import json
import random
from urllib import response
from celery import Celery
from kombu import Exchange, Queue
import time
import datetime
#import psycopg2
import uuid
#from Log_To_Database import Log
#import celeryconfig

def get_email(first_name:str,last_name:str,company_name:str,customer_id:str,priority_type:str):
    random_number = random.randint(6, 12)
    time.sleep(random_number)
    response = f"{first_name}{last_name}@{company_name}.com"
    #Log(request_x="get_email", response_x=response, customer_id_x=customer_id2,priority_type=priority_type2,sleep_time_x=random_number)
    return response

