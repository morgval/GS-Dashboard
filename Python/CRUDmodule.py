# This module initiates the MongoClient authentication, and
# defines the Create(), Read(), Update(), and Delete() and handles possible errors
# READ() is used in the DBMscript in order to populate Database data
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient
        self.client = MongoClient('mongodb://' + username + ":" + password + '@localhost:27017')
        self.database = self.client['AAC']

    """ CREATE """
    def create(self, data):
#check parameters are not empty
        if data:
            result = self.database.animals.insert_one(data)
        else:
            raise Exception("ERROR: Nothing to save, because data parameter is empty")

#check the record was found
        if result:
            print("The following data was added to the database: ")
            return result
        else:
            raise Exception("ERROR: Failed to insert document")

    """ READ """
    def read(self, data):
        # data = {key : value}

#check for search parameters (defaults to findAll method, otherwise)
        if data:
            result = self.database.animals.find(data)
        else:
            result = self.database.animals.findAll()

#check if any records were found, else push error
        if result:
            return result
        else:
            raise Exception("ERROR: No results for chosen search parameter.")

    """ UPDATE """
    def update(self, data, newData):
#check data parameters are not empty
        if data is None:
            raise Exception("ERROR: Nothing updated, no search ID specified")
        elif newData is None:
            raise Exception("ERROR: Nothing updated, no update parameter specified")
        else:
            result = self.database.animals.findOneAndUpdate(data, { "$set": newData })

#check the record was found
        if result:
            print("The following record was updated: ")
            #returns true
            return result
        else:
            raise Exception("ERROR: Nothing updated, search parameter not found")
            #returns false
            return result

    """ DELETE """
    def delete(self, data):
#check data parameter not empty
        if data:
            result = self.database.animals.delete(data)
        else:
            raise Exception("ERROR: Nothing to delete")

#check the record was found
        if result:
            print("Delete Successful")
            #returns True
            return result
        else:
            raise Exception("ERROR: Requested record was not found")
             #returns False
            return result

    if __name__=='__main__':
        app.run(debug=True)
