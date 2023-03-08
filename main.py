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
    
    def convert(self, x):
        '''
        Returns the class or data type of input as a string
        Parameter
            x: str, int, bool, dict, list
                the input data
        Returns
            str
            A string describing the data type of the input data
        '''
        if type(x) == str:
            return 'STRING' #program should identify what is a string and map accordingly in JSON schema output
        elif type(x) == int:
            return 'INTEGER' #program should identify what is an integer and map accordingly in JSON schema output
        elif type(x) == bool:
            return 'BOOLEAN' #program should identify what is a boolean and map accordingly in JSON schema output
        elif type(x) == list:
            if all(type(i) == dict for i in x):
                return 'ARRAY'
            else:
                return 'ENUM'
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
            if type(j) == dict:
                schema[i] = self.get_schema(j)
                continue
            schema[i] = {'type': self.convert(j), 'tag': '', 'description': '', 'required': False}
            #Padding: All attributes in the JSON schema should be padded with "tag" and "description" and "required"                
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
        
        schema = self.get_schema(data)
        
        if dump:
            if os.path.isdir(path):
                path = os.path.join(path, "schema.json")
            os.makedirs(os.path.dirname(path), exist_ok=True) #Making the schema directory
            with open(path, 'w') as f: #Saving the schema in schema.json file 
                json.dump(schema, f)
        return schema


if __name__ == '__main__':
    data2bots = SchemaGenerator()
    for jsonfile in glob.glob('./data/*.json'):
        print(jsonfile.split('/')[-1])
        print(data2bots.generate(jsonfile, path=f"./schema/schema_{jsonfile.split('_')[-1]}", dump=True), '\n')