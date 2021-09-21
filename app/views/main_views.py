from app.transposer import create_output, string_to_list
from flask import Blueprint, redirect, render_template
from flask import request, url_for

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')

    name = request.form["name"]
    arg_name = request.form["arg_name"]
    data_definitions = request.form["data_definitions"]
    is_csv = True #request.form["name"]
    is_enumerable = "is_enumerable" in request.form
    should_create_data_definitions = "should_create_data_definitions" in request.form
    should_create_examples = "should_create_examples" in request.form
    should_create_template = "should_create_template" in request.form

    # remove new line characters from the input
    data_definitions = data_definitions.replace("\n", "").replace("\r", "").strip()

    examples = string_to_list(data_definitions, is_csv)

    output = create_output(
        name, 
        arg_name, 
        examples,
        should_create_data_definitions, 
        should_create_examples, 
        should_create_template, 
        is_enumerable)

    return output

