import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import os

def load_portfolio(json_file):
    #script_dir = os.path.dirname(__file__)  # Directory of the current script
    #file_path = os.path.join(script_dir, json_file)  # Construct full path to JSON file

    # Directory of the current script
    script_dir = os.path.dirname(__file__)
    # Move one directory up
    parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
    # Construct full path to JSON file
    file_path = os.path.join(parent_dir, json_file)

    with open(file_path, 'r') as stock_file:
        portfolio = json.load(stock_file)
    # Used for debugging
    # print(json.dumps(portfolio, indent=2))
    
    return portfolio

def load_schema(json_schema):
    script_dir = os.path.dirname(__file__)  # Directory of the current script
    file_path = os.path.join(script_dir, json_schema)  # Construct full path to JSON file

    with open(file_path, 'r') as stock_schema:
        schema = json.load(stock_schema)
    # Used for debugging
    #print("Loaded Schema:")
    #print(json.dumps(schema, indent=2))
    return schema

def validate_portfolio(portfolio, schema):
    try:
        validate(instance=portfolio, schema=schema)
        print("Portfolio validated successfully. -validator.py")
        return portfolio  # Return the validated portfolio
    except ValidationError as e:
        print("Validation of stock file failed! -validator.py")
        print(f"Error message: {e.message}")
        return None  # Return None on validation failure


# Load portfolio and schema
portfolio = load_portfolio('stock.json')
schema = load_schema('stock-schema.json')

""" Used for Debugging Validation """
'''
validated_portfolio = validate_portfolio(portfolio, schema)
if validated_portfolio:
    print("Validation passed, ready to proceed.")
    print(validate_portfolio) 
else:
    print("Validation Failed. Unable to perform calculations.")
'''