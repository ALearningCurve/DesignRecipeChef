"""Helps to convert data into design recipe steps
"""
from typing import Tuple
from enum import Enum

class DataTypes(Enum):
    """Represents the supported data types that this
    transposer module can output data for
    """
    SIMPLE = 1   # ie. Just a NaturalNumber
    ENUM = 2   
    STRUCT = 3
    
#### HELPER FUNCTIONS
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

def remove_new_lines(string: str) -> str:
    """Removes all the newline characters in a string and returns that new string

    Args:
        string (str): string to parse

    Returns:
        str
    """
    return string.replace("\n", "").replace("\r", "").strip()

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

#### CREATING EXAMPLES
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
        output += f"(define {name.upper()}-{remove_quotes(item).strip().upper()} {example_values[i]})\n"
    return output

def create_examples_struct(example_values:list, name:str) -> str:
    args = " ".join([value for value in example_values])
    return f"\n(make-{name.lower()} {args})\n"

#### CREATING DATA DEFINITIONS
def create_data_definitions_enum(example_values: list, name: str, header:str="") -> str:
    """converts list of possible datatype values (step 1 of design recipe for enums) to 
    a formatted string

    Args:
        example_values (list)
        name (str): Name of the datatype
        header (str): Alternate header for the list of items. Default ""
    Returns:
        str
    """
    output = f"; A {name} is one of:" if header == "" else header
    output += "\n"
    for item in example_values:
        output += f"; - {item} \n"
    return output

def create_data_definitions_struct(example_names: list, name:str) -> str:
    """converts list of possible datatype fields  to 
    a formatted string. This method adds suggested placeholders for a struct

    Args:
        example_names (list): Names of the fields given for this struct
        name (str): Name of the datatype

    Returns:
        str
    """
    output = f"(define-struct {name.lower()} ["
    temp = []
    for i, val in enumerate(example_names):
        temp.append(f"{val}: ...")
        output += " " if i > 0 else ""
        output += val
    output += "])\n"
    type_text = " ".join(["TYPE" for x in example_names])
    output += create_data_definitions_enum(temp, name, f"A {name} is a (make-{name.lower()} {type_text})")
    return output

#### CREATING TEMPLATES
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
    output += f"(define ({datatype_name.lower()}-temp {arg_name})"
    output += f"\n  (cond [({comparison_operator} {arg_name} {datatype_name.upper()}-{remove_quotes(example_names[0]).strip().upper()}) ...]"
    for i in range(1, len(example_names)):
        output += f"\n        [({comparison_operator} {arg_name} {datatype_name.upper()}-{remove_quotes(example_names[i]).strip().upper()}) ...]"
    output += "))\n"

    return output

def create_template_struct(example_names: list, datatype_name:str, arg_name: str) -> str:
    """Creates a method template (in the design recipe for a struct datatype)

    Args:
        example_names (list): names of the field of the struct
        datatype_name (str): name of the struct
        arg_name (str): name of the arg to pass into the function

    Returns:
        str: Template for a function
    """
    output = "\n"
    output += f"(define ({datatype_name.lower()}-temp {arg_name})"
    for i, name in enumerate(example_names):
        output += "\n"
        output += "  (... " if i == 0 else "       "
        output += f"({datatype_name.lower()}-{remove_quotes(name).strip()} {arg_name}) ..."
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
    output += f"(define ({datatype_name.lower()}-temp {arg_name})"
    output += f"\n  (... {arg_name} ...))"

    return output


#### CREATING OUTPUT
def create_output(name: str, arg_name: str, examples: list, should_create_data_definitions: bool, should_create_examples: bool, should_create_template: bool, data_type: DataTypes) -> str:
    """Generate the parts of the design recipe for the given examples and selected options

    Args:
        name (str): Name of the Datatype
        arg_name (str): Name of the argument to pass into the generated template
        example_names (list): Examples to use to create the output
        should_create_data_definitions (bool): Whether or not to create the data defintion section
        should_create_examples (bool): Whether or not to create the examples section
        should_create_template (bool): Whether or not to create the template section
        data_type (DataType): The type of the data
        is_csv (bool): Whether or not the data was a csv

    Returns:
        str: formatted output of all parts added together
    """
    # Check datatype is valid
    try:
        data_type = int(data_type)
        if not (data_type in set(item.value for item in DataTypes)):
            raise ValueError("Unsupportd Data Type") 
    except ValueError:
        return "\nBadRequest: Unsupported Data Type\n"

    # Start generating output
    output = "\n"
    example_names, example_values = seperate_name_and_value(examples)

    if should_create_data_definitions:
        if  data_type == DataTypes.ENUM.value:
            output += create_data_definitions_enum(example_values, name)
        elif data_type == DataTypes.STRUCT.value:
            # Rather than pass example values we want the names for the fields
            # of the struct so that they can be elaborated on later by the user
            output += create_data_definitions_struct(example_names, name)
        else: 
            output += "\n;;;;;;; TODO- Expand definition! Definitions are not supported for this datatype!\n"

    if should_create_examples:
        if data_type in (DataTypes.ENUM.value, DataTypes.SIMPLE.value):
            output += create_examples(example_names, example_values, name)
        elif data_type == DataTypes.STRUCT.value:
            output += create_examples_struct(example_values, name)
        else:
            output += "\n;;;;;;; Examples are not supported for this datatype!\n"

    if should_create_template:
        if data_type == DataTypes.ENUM.value:
            output += create_template_enum(example_names, name, arg_name)
        elif data_type == DataTypes.STRUCT.value:
            output += create_template_struct(example_names, name, arg_name)
        elif data_type == DataTypes.SIMPLE.value:
            output += create_template_simple(name, arg_name)
        else:
            output += "\n;;;;;;; Template not supported for this datatype!\n"

    output += "\n"
    if (remove_new_lines(output) == ""):
        return "<br>Could not generate any code!!!! <br>\
            - Did you select things the program should output?<br>\
            - Did you select the data type?<br><br>"
    return output

