from flask import render_template, Response, request, stream_template
from init_consumer import app, socketio
import tasks_consumer
import uuid

# # Render a template with a given context as a stream and return a TemplateStream
# def render_template_stream(template_name, **context):
#     print(context)
#     app.update_template_context(context) # Update the template context with some commonly used variables. 
#     t = app.jinja_env.get_template(template_name) # jinja2.Environment.get_template() # Load a template by name with loader and return a Template.
#     rv = t.stream(context) # jinja2.Template.stream # Return a TemplateStream that returns one function after another as strings
#     rv.enable_buffering(5) # jinja2.environment.TemplateStream.enable_buffering # Buffer 5 items before yielding them
#     return rv # Return a TemplateStream

# Registers a function to be run before the first request to this instance of the application
# Create a unique session ID and store it within the application configuration file
@app.before_request
def initialize_params():
    if not hasattr(app.config,'uid'):
        sid = str(uuid.uuid4())
        app.config['uid'] = sid
        print("initialize_params - Session ID stored =", sid)

# Render the assigned template file
@app.route("/", methods=['GET'])
def index():
    return render_template('consumer.html')
       
@app.route('/consumetasks', methods=['GET','POST'])
def getStockStatus():
    # Handle the POST request
    if request.method == 'POST':
        print("Retrieving stock status")
        return Response(stream_template('consumer.html', stockInfo = list(tasks_consumer.sendStockStatus())))     
    # Handle the GET request
    elif request.method == 'GET':
        return '''
         <!doctype html>
        <html>
            <head>
                <title>Stock Sheet</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            </head>

            <body class="container">
                <h1>Stock Sheet</h1>
                <div>
                    <button id="consumeTasks">Check stock status</button>
                </div>
            </body>
        </html>
        '''

# Run using port 5001
if __name__ == "__main__":
    socketio.run(app,host='localhost', port=5001,debug=True)