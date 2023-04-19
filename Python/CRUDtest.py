# Unit tests run in JupyterDash to test the CRUDmodule
import unittest

from CRUDmodule.py import create, read, update, delete

class TestCR(unittest.TestCase):
    #VARIABLES
    data =  {"age_upon_outcome" : "3 years",
            "animal_id" : "XY3028",
            "animal_type" : "Dog",
            "breed" : "Akita",
            "color" : "Gray",
            "date_of_birth" : "Aug 2018",
            "datetime" : """,
            "name" : "Wren",
            "outcome_subtype" : "",
            "outcome_type" : "",
            "sex_upon_outcome" : "Spayed Female",
             "age_upon_outcome_in_weeks" : "164 weeks"
             },
             
    key = {"animal_id" : "XY3028"},

    #CREATE - tests if sample data was created
    def test_create(self, data):
        result = create(data)
        self.assertTrue(result)

    #READ - assumes "animal_id" is the unique key
    def test_read(self, key, data):
        result = read(key)
        self.assertEqual(result, data)

    #UPDATE
    def test_update(self, key):
        newData = {"color" : "Black"}
        result = update(key, newData)
        self.assertTrue(result)

    #DELETE
    def test_delete(self):
        result = delete(data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
