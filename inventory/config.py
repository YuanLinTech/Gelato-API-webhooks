# Application configuration File
################################
# Secret key that will be used by Flask for securely signing the session cookie
# and can be used for other security related needs
SECRET_KEY = '6d5360f5bcaef031df544387eb9e78c041886ad0fe291ea7c05b16b23bfbf7a4'
#######################################
# Minimum number of product SKUs to send
MIN_NBR_SKUS = 1
# Maximum number of product SKUs to send
MAX_NBR_SKUS = 100
# Minimum number of tasks to send in a batch
MIN_NBR_TASKS = 1
# Maximum number of tasks to send in a batch
MAX_NBR_TASKS = 20


'''
The webhook calls are sent via an HTTP POST request every 10 minutes, 
with a list of product SKUs limited to 100 per call. 
'''
# Time to wait (in seconds) before generating and executing the next task
# Set to 15 for the purpose of testing. Should be set to 600 for actual deployment.
WAIT_TIME = 15
# URL to send the Webhook message (request) to
WEBHOOK_RECEIVER_URL = 'http://localhost:5001/consumetasks'
#######################################
# Map to the REDIS Server Port
BROKER_URL = 'redis://localhost:6379'
#######################################