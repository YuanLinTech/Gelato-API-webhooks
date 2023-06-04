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
class TaskProvider(BaseProvider):
    def SKUs():
        apparel = ["SWEATSHIRT", "TSHIRT", "HOODIE", "PFMTSHIRT"]
        manufacturer = ["CN_KD", "CN_US", "CN_WM", "LS_US","RC_US"]
        model = ["HWT","CLS","BAS","PRM"]
        size = ["S", "M", "L", "XL", "2XL","3XL"]
        colour = ["BLACK", "NAVY", "RED", "ROYAL", "ORANGE", "GOLD", "WHITE", "MAROON", "PURPLE", "CHARCOAL","DARKHEATHER",
                    "SPORTGREY", "LIGHTBLUE", "ROYALBLUE", "IRISHGREEN", "LIGHTPINK",  "MILITARYGREEN", "WHITEBLACK", "WHITERED"]
        SKU = [apparel[random.randint(0, len(apparel)-1)], manufacturer[random.randint(0, len(manufacturer)-1)],
                model[random.randint(0, len(model)-1)], size[random.randint(0, len(size)-1)], colour[random.randint(0, len(colour)-1)]]
        return SKU
    
# Create and initialise a faker generator and return data in US English
# Seeding to have the same results every time we execute the script
fakeTasks = Faker('en_US')
# Seed the Faker instance to have the same results every time we run the program
fakeTasks.seed_instance(0)
# Assign the TaskProvider to the Faker instance
fakeTasks.add_provider(TaskProvider)

# Generate A Fake Task
def produce_task():
    # Message composition
    message = {"version": "1.0", "SKU": "_".join(fakeTasks.SKUs())}
    return message

print(json.dumps(produce_task()))

'''
Webhooks will try to send the request data 3 times, with 5 seconds delay between each try, if an HTTP status 2xx is not returned.

'''
def send_webhook(msg):
    """
    Send a webhook request to a specified URL
    :param msg: task details
    :return:
    """
    try:
        # Post a webhook message
        # default is a function applied to objects that are not serializable = it converts them to str
        resp = requests.post(config.WEBHOOK_RECEIVER_URL, data=json.dumps(
            msg, sort_keys=True, default=str), headers={'Content-Type': 'application/json'}, timeout=5.0)
        # Returns an HTTPError if an error has occurred during the process (used for debugging).
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        #print("An HTTP Error occurred",repr(err))
        pass
    except requests.exceptions.ConnectionError as err:
        #print("An Error Connecting to the API occurred", repr(err))
        pass
    except requests.exceptions.Timeout as err:
        #print("A Timeout Error occurred", repr(err))
        pass
    except requests.exceptions.RequestException as err:
        #print("An Unknown Error occurred", repr(err))
        pass
    except:
        pass
    else:
        return resp.status_code