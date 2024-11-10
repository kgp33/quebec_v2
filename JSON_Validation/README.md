## JSON Validation

This folder contains three files:

    - stock-schema.json
    - stock.json
    - validator.py

### Stock-Schema.json
This is a json file that defines the expected format of json files to be ingested by our quebec pricing tool.

### Stock.json
This is an example portfolio that is formatted in the way we expect our quebec pricing tool to require. It was used to test validator.py.

### Validator.py
This is a python script that opens the example stock.json file and checks whether it matches the schema defined in stock-schema.json. This is an minimum viable product (MVP) and can be changed as the repo grows and matures. 
