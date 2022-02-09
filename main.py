import json
import os
import glob

class SchemaGenerator(object):
    '''
    A class to extract the schema from a json file
    '''
    def __init__(self, jsonfile={}):
        '''
        Initializes variables
        '''
        self.jsonfile = jsonfile
        self.schema = {}
    
    def convert(self, x):
        '''
        Returns the class or data type of input as a string
        Parameter
            x: str, int, float, bool, dict, list
                the input data
        Returns
            str
            A string describing the data type of the input data
        '''
        if type(x) == str:
            return 'STRING' #program should identify what is a string and map accordingly in JSON schema output
        elif type(x) == int:
            return 'INTEGER' #program should identify what is an integer and map accordingly in JSON schema output
        elif type(x) == float:
            return 'NUMBER' #program should identify floating point numbers and map accordingly in JSON schema output
        elif type(x) == bool:
            return 'BOOLEAN' #program should identify booleans and map accordingly in JSON schema output
        elif type(x) == dict:
            return 'OBJECT' #program should identify what when a key contains another JSON object and map accordingly in as OBJECT 
        elif type(x) == list:
            for i in x:
                if type(i) == dict: 
                    return 'ARRAY' #When the value in an array is another JSON object, the program should map the data type as an ARRAY
            return 'ENUM' #When the value in an array is a string, int, the program should map the data type as an ENUM
        else:
            return None
        
    def get_schema(self, file):
        '''
        Returns the schema of a read json file or dictionary
        Parameter
            file: dict
                A dictionary, empty or non-empty, which the schema is to be generated
        Returns
            schema: dict
                The generated dictionary using the given conditions
        '''
        schema = {} #Creating an empty dict
        for i, j in file.items():#Iterating through the input dictionary, i is the key, j is the value
            
            schema[i] = {'type': self.convert(j), 'tag': '', 'description': ''}
            #Padding: All attributes in the JSON schema should be padded with "tag" and "description"
            
            if self.convert(j) == 'OBJECT': #If an attribute contains a nested JSON object, it should be further padded
                schema[i]['properties'] = self.get_schema(j)
                schema[i]['required'] = list(j.keys())
            
            if self.convert(j) == 'ARRAY':
                '''
                These should be further padded with the key: "items" and the value would be the schema for any of the nested JSON.
                Assuming ALL members of an array have the same schema
                We will pick the first element of the list alone
                '''
                schema[i]['items'] = self.get_schema(j[0])
                schema[i]['required'] = list(j[0].keys())
                
        return schema
    
    def generate(self, jsonfile, path=".", dump=False):
        '''
        Gets the schema for the jsonfile input and saving the schema to /schema directory
        Parameters
            jsonfile: str, filepath, dict
                The jsonfile to be read as either a dictionary, a filepath of the json or json string
            path: str, filepath
                The path to dump the schema of the input json file
                Only when dump is True
            dump: bool
                Whether the json schema will be dumped in path variable
        
        Returns
            schema: dict
                The schema of the input dictionary
        '''
        if type(jsonfile) == dict:
                self.jsonfile = jsonfile
        else:
            try:
                self.jsonfile = json.loads(jsonfile) #For json string
            except ValueError:
                self.jsonfile = json.load(open(jsonfile)) #For filepath to a json file
            except Exception as e:
                raise e
        
        #Using a try loop incase the jsonfile doesn't contain a 'message' attribute
        try:
            data = self.jsonfile['message']
        except Exception as e:
            print(e)
            data = None
        if type(data) != dict: #Return an error message, when the message attribute doesnt contain a dictionary data type
            return f"message contains no schema, message is {self.convert(data)}"
        
        self.schema = self.get_schema(data)
        
        if dump:
            os.makedirs(f'{path}/schema', exist_ok=True) #Making the schema directory
            with open(f"{path}/schema/schema.json", 'w') as f: #Saving the schema in schema.json file 
                json.dump(self.schema, f)
        return self.schema

if __name__ == '__main__':
    data2bots = SchemaGenerator()
    for jsonfile in glob.glob('./data/*.json'):
        print(jsonfile.split('\\')[-1])
        print(data2bots.generate(jsonfile), '\n')
