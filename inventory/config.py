# Application configuration File
################################
# Secret key that will be used by Flask for securely signing the session cookie
# and can be used for other security related needs
SECRET_KEY = '6d5360f5bcaef031df544387eb9e78c041886ad0fe291ea7c05b16b23bfbf7a4'
#######################################
# Minimum Number Of Tasks To Generate
MIN_NBR_TASKS = 1
# Maximum Number Of Tasks To Generate
MAX_NBR_TASKS = 100
'''
The webhook calls are sent via an HTTP POST request every 10 minutes, 
with a list of product SKUs limited to 100 per call. 
'''
# Time to wait when producing tasks
WAIT_TIME = 600
# URL to send the Webhook message (request) to
WEBHOOK_RECEIVER_URL = 'http://localhost:5001/consumetasks'
#######################################
# Map to the REDIS Server Port
BROKER_URL = 'redis://localhost:6379'
#######################################