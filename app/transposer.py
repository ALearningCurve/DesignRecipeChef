from typing import Tuple

"""Example Data
    name = "CompassDirection"
    arg_name = "".join([char for char in name if char.isupper()]).lower()
    data_definitions = '"N","NE","E","SE","S","SW","W","NW"'
    is_csv = True
    is_enumerable = True
    should_create_data_definitions = True
    should_create_examples = True
    should_create_template = True
    output = create_output(name, arg_name, input_handler(data_definitions, is_csv), should_create_data_definitions, should_create_examples, should_create_template, is_enumerable)

"""
def data_definitions_to_list(string: str) -> list:
    """Convert enum data definition from design recipe to a list of strings for each enum's definitions

    Args:
        string (str): Data definition as a string to convert

    Returns:
        list: of strings
    """
    string = string.strip()
    parts = string.split("; - ")

    while ("" in parts):
        parts.remove("")
    
    print(parts)
    return parts

def remove_quotes(string: str) -> str:
    """removes " from strings

    Args:
        string (str): string to parse

    Returns:
        str: without quotation marks
    """
    string = string.strip()
    string = string.replace("\"", "")
    return string

def create_examples(example_names: list, example_values: list, name: str) -> str: 
    """Converts list of examples and values (step 3 of design recipe) to define statements

    Args:
        example_names (list): list of examples to use to create the example string
        example_values (list): List of values to pair with eacha name
        name (str): The name of the data type 

    Returns:
        str: formatted string
    """
    output = "\n"
    for i, item in enumerate(example_names):
        output += f"(define {name.upper()}-{remove_quotes(item).strip()} {example_values[i]})\n"
    return output
        
def create_data_definitions(example_values: list, name: str) -> str:
    """converts list of possible datatype values (step 1 of design recipe for enums) to 
    a formatted string

    Args:
        example_values (list)
        name (str): Name of the datatype

    Returns:
        str
    """
    output = "\n"
    output = f"; A {name} is one of: \n"
    for item in example_values:
        output += f"; - {item} \n"
    return output

def create_template_enum(example_names: list, datatype_name: str, arg_name: str) -> str:
    """Creates a method template (in the design recipe) for an enum datatype

    Args:
        example_names (list): example name used for each example definition
        datatype_name (str): Name of the datatype
        arg_name (str): Name of the arg used in this template

    Returns:
        str: Template for a function
    """
    comparison_operator = "string=?"
    output = "\n"
    output += f"(define ({datatype_name.lower()}-template {arg_name})"
    output += f"\n  (cond [({comparison_operator} {arg_name} {datatype_name.upper()}-{remove_quotes(example_names[0]).strip()}) ...]"
    for i in range(1, len(example_names)):
        output += f"\n        [({comparison_operator} {arg_name} {datatype_name.upper()}-{remove_quotes(example_names[i]).strip()}) ...]"
    output += "))\n"

    return output

def create_template_simple(datatype_name: str, arg_name: str) -> str:
    """Creates a generic method template for an simple datatype


    Args:
        datatype_name (str): Name of the datatype
        arg_name (str): Name of the arg that is being passed into this template

    Returns:
        str: Simple method stub/template
    """
    output = "\n"
    output += f"(define ({datatype_name}-template {arg_name})"
    output += f"\n  (... {arg_name} ...))"

    return output


def string_to_list(input:str, is_csv: bool) -> list:
    """Converts string user entered into a list of items
    in that string. Supports data definition format as 
    seen in racket and csv values

    Args:
        input (str): string to parse into an array
        is_csv (bool): Wether or not that string is a csv

    Returns:
        list: of strings
    """
    if not is_csv:
        return data_definitions_to_list(input)
    else:
        return input.strip().split(",")

def seperate_name_and_value(list: list) -> Tuple[list, list]:
    """Seperate name and value for examples in provided list. 
    Items should be seperated by '::'

    Args:
        list (list): list of examples as strings

    Returns:
        Tuple[list, list]: the list of names and the list of values
    """
    names = [item.split("::")[0] for item in list]
    values = [item.split("::")[-1] for item in list]
    return names, values

def create_output(name: str, arg_name: str, examples: list, should_create_data_definitions: bool, should_create_examples: bool, should_create_template: bool, is_enumerable: bool) -> str:
    """Generate the parts of the design recipe for the given examples and selected options

    Args:
        name (str): Name of the Datatype
        arg_name (str): Name of the argument to pass into the generated template
        example_names (list): Examples to use to create the output
        should_create_data_definitions (bool): Whether or not to create the data defintion section
        should_create_examples (bool): Whether or not to create the examples section
        should_create_template (bool): Whether or not to create the template section
        is_enumerable (bool): Whether or not the data is an enumerable type

    Returns:
        str: formatted output of all parts added together
    """
    output = "\n"
    example_names, example_values = seperate_name_and_value(examples)

    if should_create_data_definitions:
        if is_enumerable:
            output += create_data_definitions(example_values, name)
        else: 
            output += ";;;;;;; TODO- Expand definition!\n"

    if should_create_examples:
        output += create_examples(example_names, example_values, name)

    if should_create_template:
        if is_enumerable:
            output += create_template_enum(example_names, name, arg_name)
        else:
            output += create_template_simple(name, arg_name)
    output += "\n"
    return output

