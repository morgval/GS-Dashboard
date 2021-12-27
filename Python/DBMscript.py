#!/usr/bin/python
from CRUDmodule import AnimalShelter

def main():
    # DICTIONARY STRUCTURE FOR AAC
    # data = {"age_upon_outcome" : age,
    #         "animal_id" : animalID,
    #         "animal_type" : animalType,
    #         "breed" : breed,
    #         "color" : color,
    #         "date_of_birth" : DOB,
    #         "datetime" : Date(),
    #         "name" : name,
    #         "outcome_subtype" : subtype,
    #         "outcome_type" : outcomeType,
    #         "sex_upon_outcome" : sex,
    #          "age_upon_outcome_in_weeks" : ageInWeeks
    #     }
    username = input("Please enter username: ")
    password = input("Please enter password: ")
    access = __init__(username, password)
    if access:
        chosenFunc = input("What would you like to access? Please enter C, R, U, or D.")
        if chosenFunc == 'C':
            animal_id = input("Enter ID number: ")
            name = input("What is the name?")
            sex = input("Please specify sex and intact: ")
            animal_type = input("What type of animal? Dog, Cat, or Monkey?")
            breed = input("What breed?")
            color = input("What color?")
            DOB = input("Enter birthdate, if known: ")
            ageInYears = input("Enter age (in years): ")
            ageInWeeks = input("Enter age (in weeks): ")
            outcomeType = input("Enter outcome type: ")
            subtype = input("Enter outcome subtype: ")
            data = {"age_upon_outcome" : age,
                     "animal_id" : animalID,
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
            return create(data)

        elif chosenFunc == 'R':
            key = input("Enter key to be searched: (Leave blank to search all) ")
            value = input("Enter value to be searched: (Leave blank to search all) ")
            data = { key : value }
            return read(data)

        elif chosenFunc == 'U':
            animalID = input("Enter the ID of the record you want to update: ")
            newKey = input("Enter the property you want to update (please reference documentation): ")
            newValue = input("Enter the value you want to change it to: ")
            data = { "animal_id" : animalID }
            if newKey or newValue is None:
                newData is None
            else:
                newData = { newKey : newValue }
            return update(data, newData)

        elif chosenFunc == 'D':
            animalID = input("Enter the ID of the record you want to delete: ")
            data = { "animal_id" : animalID }
            return delete(data)

    else:
        raise Exception("UNABLE TO VERIFY CREDENTIALS")
