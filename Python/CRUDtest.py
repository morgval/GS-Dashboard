import unittest

from CRUD.py import create, read, update, delete

class TestCR(unittest.TestCase):
    #CREATE
    def test_create(self):
        data =  {"age_upon_outcome" : "3 years",
                "animal_id" : "XY3028",
                "animal_type" : "Dog",
                "breed" : "Akita",
                "color" : "Gray",
                "date_of_birth" : "Aug 2018",
                "datetime" : Date(),
                "name" : "Wren",
                "outcome_subtype" : "",
                "outcome_type" : "",
                "sex_upon_outcome" : "Spayed Female",
                 "age_upon_outcome_in_weeks" : "164 weeks"
                 }
        result = create(data)
        self.assertTrue(result)

    #READ
    def test_read(self):
        data = {"animal_id" : "XY3028"}
        match = {"age_upon_outcome" : "3 years",
                "animal_id" : "XY3028",
                "animal_type" : "Dog",
                "breed" : "Akita",
                "color" : "Gray",
                "date_of_birth" : "Aug 2018",
                "datetime" : Date(),
                "name" : "Wren",
                "outcome_subtype" : "",
                "outcome_type" : "",
                "sex_upon_outcome" : "Spayed Female",
                 "age_upon_outcome_in_weeks" : "164 weeks"
                 }
        result = read(data)
        self.assertEqual(result, match)

    #UPDATE
    def test_update(self):
        data = {"animal_id" : "XY3028"} 
        newData = {"color" : "Black"}
        result = update(data, newData)
        self.assertTrue(result)

    #DELETE
    def test_delete(self):
        data = {"animal_id" : "XY3028"}
        result = delete(data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
