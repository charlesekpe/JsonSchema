#!/usr/bin/env python
# coding: utf-8

# In[86]:


import pytest
import json
from main import SchemaGenerator


# In[ ]:


@pytest.fixture
def example_schema():
    '''Returns a Schema for example_input.json'''
    sch = SchemaGenerator()
    with open('./examples/example_input.json') as f:
        data = json.load(f)
    schema = sch.generate(data)
    return data, schema
def test_string:
    assert type(string) == str
