from flask import Response, render_template
from init_producer import app
import tasks_producer

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@app.route("/", methods=['GET'])
def index():
    return render_template('producer.html')

@app.route('/producetasks', methods=['POST'])
def producetasks():
    print("Producing tasks")
    return Response(stream_template('producer.html', data = tasks_producer.produce_bunch_tasks()))

# Stop the app.run() function from being automatically executed when the app_producer.py file is imported as a module to another file.
if __name__ == "__main__":
   app.run(host="localhost",port=5000, debug=True)
