from connector import *

def get_all_authors():
    query = "SELECT id, name FROM authors"
    return executeDictQueryNoParams(query)
