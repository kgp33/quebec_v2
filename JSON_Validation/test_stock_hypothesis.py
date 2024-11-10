import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from hypothesis import given
from hypothesis import strategies as st
from hypothesis_jsonschema import from_schema

#load the JSON schema file
with open ('stock-schema.json') as stock_schema:
    schema = json.load(stock_schema)

#function to make sure that Hypotheis generated stocks are valid per schema 
def validate_portfolio(portfolio):
    for stock in portfolio:
        validate(instance=stock, schema=schema)

#using @given indicates a test function should receive automatically generated input data
#if this test fails, we know theres an issue with how we're handling valid input
@given(from_schema(schema))
def test_valid_portfolio(portfolio):
    #print whats being generated
    print(portfolio)
    validate(instance=portfolio, schema=schema)
    

#this is generating and testing invalid input
#st.lists is a hypothesis strategy used to generate lists
#st.one_of is a hypothesis strategy that lets you specify multiple strategies
@given(st.lists(st.one_of(
    #this is going to generate valid stock entries based on schema
    from_schema(schema),
    #this is going to generate invalid stock entries that are zero or positive, which is invalid because schema indicates that a stock is an object, not an integer.
    st.integers(min_value=0),
    #this is going to generate dictionaries with random keys and integer values that have unexpected properties not allowed per the schema. 
    st.dictionaries(
            #this is going to generate the dictionaries' keys
            keys=st.text(),
            #this is going to generate the dictionaries' values
            values=st.integers()
        )
    ),
    #this makes sure the list generated has at least one element
    min_size=1
)
)

#this function will validate a portfolio that has both valid and invalid entries and makes sure code can handle both
#it allows for failures in invalid entries and logs those failures without causing whole test to fail
#if this test fails, we know there's an issue with how invalid entries are processed.
def test_valid_invalid_portfolio(portfolio):
    #validate valid stocks and iterate over each stock in portfolio
    for stock in portfolio:
        #checks that the stock is a dictionary, which is an object and then checks that the dictionary has ticker and nShares, which are required per the schema
        if isinstance(stock, dict) and 'ticker' in stock and 'nShares' in stock:
            try:
                validate(instance=stock, schema=schema)
            except ValidationError:
                print(f"{stock['ticker']} failed validation, moving to next stock.")
                continue