from flask import Response, render_template, stream_template
from init_producer import app
import tasks_producer

# # Render a template with a given context as a stream and return a TemplateStream
# def render_template_stream(template_name, **context):
#     app.update_template_context(context) # Update the template context with some commonly used variables. 
#     t = app.jinja_env.get_template(template_name) # jinja2.Environment.get_template() # Load a template by name with loader and return a Template.
#     rv = t.stream(context) # jinja2.Template.stream # Return a TemplateStream that returns one function after another as strings
#     rv.enable_buffering(5) # jinja2.environment.TemplateStream.enable_buffering # Buffer 5 items before yielding them
#     return rv # Return a TemplateStream

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
