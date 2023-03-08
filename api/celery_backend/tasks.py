
from celery.utils.log import get_task_logger 
from kombu import Exchange, Queue
import json
#import api.celery_backend.celery_tasks as task_import
from celery import Celery

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)




app = Celery("app", broker="amqps://ap:RabbitMQ-23@mq1.egrabber.net:5671",backend="rpc://")



High_Priority_Exchange= Exchange("High_Priority_Exchange",type="direct")

Heavy_Workload_Exchange1= Exchange("Heavy_Workload_Queue1",type="direct")
Heavy_Workload_Exchange2= Exchange("Heavy_Workload_Queue2",type="direct")

Low_Workload_Exchange1= Exchange("Low_Workload_Queue1",type="direct")
Low_Workload_Exchange2= Exchange("Low_Workload_Queue2",type="direct")


app.conf.task_queues = [ 
    Queue("High_Priority_Queue_BT", High_Priority_Exchange, routing_key="High_Priority_Exchange_BT",queue_arguments={'x-max-priority': 10}),
    Queue("High_Priority_Queue_ST", High_Priority_Exchange, routing_key="High_Priority_Exchange_ST",queue_arguments={'x-max-priority': 10}),
    Queue("Heavy_Workload_Queue1", Heavy_Workload_Exchange1, routing_key="Heavy_Workload_Queue1",queue_arguments={'x-max-priority': 10}),
    Queue("Heavy_Workload_Queue2", Heavy_Workload_Exchange2, routing_key="Heavy_Workload_Queue2",queue_arguments={'x-max-priority': 2}),
    Queue("Low_Workload_Queue1",  Low_Workload_Exchange1, routing_key="Low_Workload_Queue1",queue_arguments={'x-max-priority': 2}),
    Queue("Low_Workload_Queue2",  Low_Workload_Exchange2, routing_key="Low_Workload_Queue2",queue_arguments={'x-max-priority': 2}),
    ]


# specify the routing key for each task
app.conf.task_routes = {
    "tasks.proces_task": {"queue": "High_Priority_Queue_BT", "routing_key": "High_Priority_Exchange_BT"},
    "tasks.proces_task": {"queue": "High_Priority_Queue_ST", "routing_key": "High_Priority_Exchange_ST"},
    "tasks.proces_task": {"queue": "Heavy_Workload_Queue1", "routing_key": "Heavy_Workload_Queue1"},
    "tasks.proces_task": {"queue": "Heavy_Workload_Queue2", "routing_key": "Heavy_Workload_Queue2"},
    "tasks.proces_task": {"queue": "Low_Workload_Queue1", "routing_key": "Low_Workload_Queue1"},
    "tasks.proces_task": {"queue": "Low_Workload_Queue2", "routing_key": "Low_Workload_Queue2"},
}
    




@app.task(name='process_task',worker_prefetch_multiplier=0,prefetch_multiplier=0)#,acks_late=True,task_track_started=True)
def process_task(first_name:str,last_name:str,company_name:str,customer_id:str,priority_type:str):
    import api.celery_backend.celery_tasks as asd
    response = asd.get_email(first_name,last_name,company_name,customer_id,priority_type)
    #response_json = json.loads(response)
    return response









