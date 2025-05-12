from connector import *

def get_all_genres():
    query = "SELECT id, genre FROM genres"
    return executeDictQueryNoParams(query)
