
from sqlite3 import TimestampFromTicks
import uuid
from celery import group
from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMddleware
#from api.router import router_tasks
from celery.result import AsyncResult
import random
from fastapi import APIRouter, HTTPException, Query,UploadFile,File
from fastapi.responses import JSONResponse
import json
from api.celery_backend.tasks import process_task
import api.celery_backend.tasks as backend_celery_task
from api.methods.Load_Data_From_File_To_A_List import load_data_from_file_to_a_list
from fastapi.responses import FileResponse
import pandas as pd
#Fetch_Data 
#from  models import *
job_list=[]



app=FastAPI()

task_id_list= []
xyz_list=[]
xyz_dict={}
global_dict = {}
global_dataframe =pd.DataFrame()
progress_bar = 0
global_unique_filename = str(uuid.uuid4())


User_Request_Details = {}
result_list=[]
result_dict={}

@app.get('/')
def touch () :
    return 'API is running'



@app.post('/send-requests')
def post_user_file(customer_id:str,file:UploadFile= File(...)):
    global progress_barw 
    content_list = []
    content_list =load_data_from_file_to_a_list(file)
    #print(content_list)
    job_list=[]
    #upper_range = len(content_list)
    upper_range = 10
    queue_assigned = (f'Heavy_Workload_Queue{random.randrange(1,3)}'if upper_range >2 else f'Low_Workload_Queue{random.randrange(1,3)}')
    priority_list = [1,5,9]
    if customer_id in priority_list:
        priority_type='PRIORITY'
        queue_assigned = ('High_Priority_Queue_BT'if upper_range >2 else 'High_Priority_Queue_BT')

    else:
        priority_type = 'NOT_PRIORITY'
        queue_assigned = (f'Heavy_Workload_Queue{random.randrange(1,3)}'if upper_range >2 else f'Low_Workload_Queue{random.randrange(1,3)}')
    
    first_name_list=[]
    last_name_list=[]
    company_name_list=[]
    for i in range(0,upper_range):
        print(queue_assigned)
        job_list.append(backend_celery_task.process_task.s(content_list[i]['First Name'],content_list[i]['Last Name'],content_list[i]['Company'],customer_id,priority_type))
        first_name_list.append(content_list[i]['First Name'])
        last_name_list.append(content_list[i]['Last Name'])
        company_name_list.append(content_list[i]['Company'])
    job = group(job_list)  
    result = job.apply_async(queue=queue_assigned,routing_key=queue_assigned)
    global_dict[global_unique_filename ] = result
    
    ##progress_bar= result.completed_count()
    ##print("result.comcnt()",result.completed_count())
    ##print(progress_bar)

   
    #result_list = result.get()
    #df = pd.DataFrame(list(zip(first_name_list,last_name_list,company_name_list,result_list)), columns =['First Name', 'Last Name','Company Name','Email']) 


    ##progress_barw = result.completed_count()
    ##print("result.comcnt()",result.completed_count())
    ##print(progress_barw)
    ##print("df",df)
    ##x = df.to_csv('outputtty.csv', encoding='utf-8', index=False)
    #print(x)
    #return FileResponse('outputtty.csv')
    #return x
    #return {"Sucess":"Item Posted!"}
    try:
        return {"file_name":global_unique_filename}
    finally:
        global global_dataframe
        result_list = result.get()
        global_dataframe = pd.DataFrame(list(zip(first_name_list,last_name_list,company_name_list,result_list)), columns =['First Name', 'Last Name','Company Name','Email']) 
        global_dataframe.to_csv(global_unique_filename, encoding='utf-8', index=False)

@app.get('/progress/{unique_id}')
def get_task_status(unique_id:str):
    
    global global_dict
    try:
        status = global_dict[unique_id]
        result = status.completed_count()
        return result+1
    except:
        return "Error "

@app.get('/get-result/{unique_id}')
def get_task_status(unique_id:str):
    global global_unique_filename
    return FileResponse(global_unique_filename)



      

