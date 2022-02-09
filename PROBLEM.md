# Objective
Write a generic program that:
- Reads a JSON file similar to what's present in this location (./data/)
- Sniffs the schema of the JSON file 
- Dumps the output in (./schema/)

# Additional informations for test cases
- Padding: All attributes in the JSON schema should be padded with `"tag"` and `"description"` keys whose values would be empty strings.
- The schema output must capture ONLY the attributes within the "message" key of the input JSON source data (see line 8 in the input JSON files). All attributes within the key "attributes" should be excluded
- For data types of the JSON schema:
  - STRING: program should identify what is a string and map accordingly in JSON schema output
  - INTEGER: program should identify what is an integer and map accordingly in JSON schema output
  - NUMBER: program should identify floating point numbers and map accordingly in JSON schema output
  - BOOLEAN: program should identify booleans and map accordingly in JSON schema output
  - OBJECT: program should identify what when a key contains another JSON object and map accordingly in as OBJECT
  - ENUM: When the value in an array is a string, the program should map the data type as an ENUM 
  - ARRAY: When the value in an array is another JSON object, the program should map the data type as an ARRAY 
- Conditional Padding: 
  - OBJECT: If an attribute contains a nested JSON object, it should be further padded with ...
    - the key: `"properties"` and the value would be the schema for the nested JSON
    - the key: `"required"` and the value would be the keys in the `"properties"` field above
  - ARRAY: These should be further padded with the key: `"items"` and the value would be the schema for any of the nested JSON. Assume ALL members of an array have the same schema

# Example of input and expected output
./examples/

# Grades
1. Does your program work and does it return the expected output (40%)
2. Did you follow software best practices and python coding standard  (25%)
3. Did you write tests for your program (unittest, pytest, etc.) (25%)

# Submission
- Create a GitHub repo, push your project and send us the link
- Add all dependencies to enable program run successfully in a requirements file
- A separate main.py should be use for executing the program seamlessly
- Provide any necessary information for running the program in README.md