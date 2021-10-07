from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        username = input("Enter username: ")
        password = input("Enter password: ")
        self.client = MongoClient('mongodb://' + username + ":" + password + '@localhost:27017')
        self.database = self.client['AAC'] 
        
# Create
    def create(self, data):
        data = {"age_upon_outcome" : age, 
                "animal_id" : ID, 
                "animal_type" : animalType, 
                "breed" : breed, 
                "color" : color, 
                "date_of_birth" : DOB, 
                "datetime" : Date(),
                "name" : name, 
                "outcome_subtype" : subtype,
                "outcome_type" : outcomeType,
                "sex_upon_outcome" : sex,
                 "age_upon_outcome_in_weeks" : ageInWeeks
            }

        if data is not None:
            self.database.animals.insert_one(data)  # data should be dictionary
            # return True #for unit testing purposes
        else:
            raise Exception("Nothing to save, because data parameter is empty")

# Read
    def read(self, data):
        data = {key : value}
        if data is not None:
            result = self.database.animals.find(data)  # data should be dictionary  
            return dumps(result) #edit to return JSON output 
        else:
            raise Exception("Nothing to read, because data parameter could not be found")

   
# Update
    def update(self, data, newData):
        data = {key : value}
        newData = {key : value}
        if data and newData is not None:
            self.database.animals.update(data, { "$set": newData })
            # return True #for unit testing purposes
        else:
            raise Exception("Nothing to update, data parameter could not be found")
            
# Delete
    def delete(self, data):
        data = {key : value}
        if data is not None:
            self.database.animals.delete(data)
            print("Delete Successful")
            # return True #for unit testing purposes
        else:
            raise Exception("Nothing to delete")
      
    if __name__=='__main__':
        app.run(debug=True)
