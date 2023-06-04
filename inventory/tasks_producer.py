# tasks_producer.py
import random
from faker import Faker
from faker.providers import BaseProvider
import config
import time
import requests
import json
import uuid

# Define a TaskProvider
# Create and initialise a Faker generator and return data in US English
# Seeding to have the same results every time we execute the script
fakeTasks = Faker('en_US')
# Seed the Faker instance to have the same results every time we run the program
fakeTasks.seed_instance(0)

# Define a TaskProvider
class TaskProvider(BaseProvider):
    def SKUs(self):
        apparel = ["SWEATSHIRT", "TSHIRT", "HOODIE", "PFMTSHIRT"]
        manufacturer = ["CN_KD", "CN_US", "CN_WM", "LS_US","RC_US"]
        model = ["HWT","CLS","BAS","PRM"]
        size = ["S", "M", "L", "XL", "2XL","3XL"]
        colour = fakeTasks.color_name()
        SKU = [apparel[random.randint(0, len(apparel)-1)], manufacturer[random.randint(0, len(manufacturer)-1)],
                model[random.randint(0, len(model)-1)], size[random.randint(0, len(size)-1)], colour.upper()]
        return SKU

# Assign the TaskProvider to the Faker instance
fakeTasks.add_provider(TaskProvider)

# Generate a fake task
def produce_task(batchid, taskid):
    # SKU list composition
    SKUList = []
    for _ in range(random.randint(config.MIN_NBR_SKUS, config.MAX_NBR_SKUS)):
        SKUList.append("_".join(fakeTasks.SKUs()))

    # Message composition
    message = {"version": "1.0", 'batchid': batchid, 'requestid': taskid, "SKU": SKUList}
    return message

# Send a webhook request to a specified URL
def send_webhook(msg):
    try:
        # Post a webhook message
        # default is a function applied to objects that are not serializable = it converts them to str
        resp = requests.post(config.WEBHOOK_RECEIVER_URL, data=json.dumps(msg, sort_keys=True, default=str), 
                             headers={'Content-Type': 'application/json'}, timeout=1.0)
        # Raises an HTTPError if an error has occurred during the process (used for debugging).
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("An HTTP Error occurred", repr(err))
    except requests.exceptions.ConnectionError as err:
        print("An Error Connecting to the API occurred", repr(err))
    except requests.exceptions.Timeout as err:
        print("A Timeout Error occurred", repr(err))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred", repr(err))
    finally:
        return resp.status_code
    
'''
Webhooks will try to send the request data 3 times, with 5 seconds delay between each try, 
if an HTTP status 2xx is not returned.

'''

# Execute Fake Tasks
def produce_bunch_tasks():
    n = random.randint(config.MIN_NBR_TASKS, config.MAX_NBR_TASKS)
    batchid = str(uuid.uuid4())
    for i in range(n):
        msg = produce_task(batchid, i)
        resp = send_webhook(msg)
        for _ in range(2):
            if (resp >= 300):
                time.sleep(5)
                resp = send_webhook(msg)
            else:
                break
        print(i, "out of ", n, " -- Status", resp, " -- Message = ", msg)
        time.sleep(config.WAIT_TIME)
        # yield resp, n, msg