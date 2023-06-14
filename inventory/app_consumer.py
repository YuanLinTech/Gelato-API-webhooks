from flask import Response, render_template, request
from flask_socketio import join_room
from init_consumer import app, socketio
import tasks_consumer
import json, uuid

# Render a template with a given context as a stream and return a TemplateStream
def render_template_stream(template_name, **context):
    app.update_template_context(context) # Update the template context with some commonly used variables. 
    t = app.jinja_env.get_template(template_name) # jinja2.Environment.get_template() # Load a template by name with loader and return a Template.
    rv = t.stream(context) # jinja2.Template.stream # Return a TemplateStream that returns one function after another as strings
    rv.enable_buffering(5) # jinja2.environment.TemplateStream.enable_buffering # Buffer 5 items before yielding them
    return rv # Return a TemplateStream

# Render the assigned template file
@app.route("/", methods=['GET'])
def index():
    return render_template('consumer.html')

# Send a message through the websocket
# Emit a SocketIO event back to the client
def send_message(event, namespace, room, message):
    print("Message = ", message)
    socketio.emit(event, message, namespace=namespace, room=room)

# Create a unique session ID and store it within the application configuration file
sid = str(uuid.uuid4())
app.config.update({'uid': sid})
print("initialize_params - Session ID stored =", sid)

# Receive the webhook requests and emit a SocketIO event back to the client
@app.route('/consumetasks', methods=['POST'])
def consume_tasks():
    if request.method == 'POST':
        data = request.json
        if data:
           print("Received Data = ", data)
           roomid =  app.config['uid']
           var = json.dumps(data)
           send_message(event='msg', namespace='/collectHooks', room=roomid, message=var)
    return data

@app.route('/getstockstatus', methods=['POST'])
def get_stock_status():
    print("Retrieving stock status")
    return Response(render_template_stream('consumer.html', stockStatus = tasks_consumer.produce_bunch_tasks()))            
    
# Execute on connecting
@socketio.on('connect', namespace='/collectHooks')
def socket_connect():
    # Display message upon connecting to the namespace
    print('Client Connected To NameSpace /collectHooks - ', request.sid)

# Execute on disconnecting
@socketio.on('disconnect', namespace='/collectHooks')
def socket_connect():
    # Display message upon disconnecting from the namespace
    print('Client disconnected From NameSpace /collectHooks - ', request.sid)

# Execute upon joining a specific room
@socketio.on('join_room', namespace='/collectHooks')
def on_room():
    if app.config['uid']:
        room = str(app.config['uid'])
        # Display message upon joining a room specific to the session previously stored.
        print(f"Socket joining room {room}")
        join_room(room)

# Execute upon encountering any error related to the websocket
@socketio.on_error_default
def error_handler(e):
    # Display message on error.
    print(f"socket error: {e}, {str(request.event)}")

# Run using port 5001
if __name__ == "__main__":
    socketio.run(app,host='localhost', port=5001,debug=True)
