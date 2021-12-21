[Company Synopsis](#company-synopsis)  
[Project Synopsis](#project-synopsis)  
[Setting Up](#setting-up)  
[Script Reference](#DBMscript)  

In progress:
- [ ] fixing SchemaValidationError
- [ ] adding selected rows callback

# Grazioso Salvare Animal Serivces
## Company Synopsis
Grazioso Salvare (GS) is a rescue animal training company that was established in 1965.  With locations in Chile, Greece, Japan, Madagascar, Singapore, South Korea, Turkey, and the US, they obtain dogs from local breeders and animal shelters to put though training regimens and then into service.   They also work with cats and monkeys.

## Project Synopsis
### Problem
GS has a new opportunity to train service animals for local law enforcement agencies.  In order to do so, all of their locations must be able to share records, adding, deleting, and modifying records appropriately.  They also need a way to read records with certain specifications to easily find what dogs will be appropriate for which type of work: 
* water rescue (looking for intact female dogs, between 26 and 156 weeks old, that are either Lab mixes, Chesapeake Bay Retrievers or Newfoundlands)
* mountain/wilderness rescue (looking for intact male dogs, between 26 and 156 weeks old, that are either German Shepherds, Alaskan Malamutes, Old English Sheepdogs, Siberian Huskies or Rottweilers), and
* disaster/rescue tracking (looking for intact male dogs, between 20 and 300 weeks old, that are either German Shepherds, Doberman Pinscher, Golden Retriever, Bloodhound or Rottweilers).
The purpose of this system is to implement a database solution that will allow GS to keep their records maintainable across their several countries of operation, in addition to developing a reusable algorithm to make their animal search more relevant to their specified queries.
The GS team decided a web based application would be most efficient, and users have also requested implementing charts and maps to better illustrate the data to help the selection team make decisions during the search process.  They have also requested a script that can be used to run CRUD functions on their database.

### Solution
My solution consists of three parts: the Python script to manipulate database from command line with full user access privileges; the web application that reads data from database and illustrates certain queries through a chart and geolocation map; and the Python module that is imported to the script and web application to support function for accessing and manipulating the database.
#### [Web Application](../Python/DB_Dashboard.py)
The primary use case for this system is a browser based dashboard that will display database data, as well as query options for finding animals for each specific type of service (water rescue, wilderness rescue, and tracking).  In addition to implementing the provided Python module to utilize the read function, the service filters are supplied by the following MongoDB queries:
```python
# Water Rescue 
  {"$and": [
      {"sex_upon_outcome":"Intact Female"},
      {"age_upon_outcome_in_weeks":{"$gte": 26}},
      {"age_upon_outcome_in_weeks":{"$lte": 156}},
      {"$or": [
           {"breed": "Labrador Retriever Mix"},
           {"breed": "Chesapeake Bay Retriever"},
           {"breed": "Newfoundland"},
      ]}
  ]}
# Wilderness Rescue 
	{"$and": [
      {"sex_upon_outcome":"Intact Male"},
      {"age_upon_outcome_in_weeks": {"$gte": 26}},
      {"age_upon_outcome_in_weeks": {"$lte": 156}},
      {"$or": [
           {"breed":"German Shepherd"},
           {"breed":"Alaskan Malamute"},
           {"breed":"Old English Sheepdog"},
           {"breed":"Siberian Husky"},
           {"breed":"Rottweiler"}
      ]},
	]}
# Tracking 
	{"$and": [
      {"sex_upon_outcome":"Intact Male"},
      {"age_upon_outcome_in_weeks": {"$gte": 20}},
      {"age_upon_outcome_in_weeks": {"$lte": 300}},
      {"$or": [
           {"breed":"German Shepherd"},
           {"breed":"Doberman Pinscher"},
           {"breed":"Golden Retriever"},
           {"breed":"Bloodhound"},
           {"breed":"Rottweiler"}
      ]}
  ]}
```
The dashboard uses Plotly Dash and Dash Leaflet to display and populate a Data Table, a pie chart with the percentage of each breed available based on the query, and a map that shows the location of the dogs in the search (IN DEVELOPMENT: I want to implement a selected rows callback to focus on one record of the map at a time).

#### [Script](../Python/DBMscript.py)
Every database needs a method for users to create, find, modify, and remove records.  For security purposes, GS requires their primary database functions (CRUD) to be limited to local operation and not web based.  Our solution is a command line script that can be run by GS administrators.  The script also imports the Python CRUD module to perform these functions on the database, while also prompting them to create the data they need to enter.  This is more efficient for GS as they do not need to train their administrators in MongoDB querying, only provide required documentation for this program.

#### [Python Module](../Python/CRUDmodule.py)
In addition to outlining CRUD functions, the Python module ensures proper user access to database by taking in username and password data for authentication.  It also supports handling for the following common user errors:
| Phase	| Error	| Reason |
| ----- | ----- | ------ |
| CREATE | Nothing to save, because data parameter is empty |	User did not enter required information for record to be inserted
| CREATE	| Failed to insert document |	Insert() function returned false, ensure server connection, or duplicate record
| READ	| No results for chosen search parameter |	Read() function did not return any results
| UPDATE	| Nothing updated, no search ID specified |	User did not enter the ID of the record they wish to update
| UPDATE	| Nothing updated, no update parameter specified |	User did not enter the key or value they want to update
| UPDATE	| Nothing updated, search parameter not found |	findOneAndUpdate() returned false.  Ensure specified record exists
| DELETE	| Nothing to delete |	User did not enter the ID to remove
| DELETE	| Requested record was not found |	Delete() returned false.  Specified record might not exist


## Setting Up
### Running the Mongo Server
For this application, we used the document-oriented database program MongoDB.  I have simply utilized the free, open-source community version to run locally.  This README assumes operation on Windows 10, but you can email me if you would like directions for installing on Linux Ubuntu.
#### Installation
You will want to install the following Mongo packages:
* [MongoDB Community Server](https://www.mongodb.com/try/download/community) 
* [MongoDB Tools](https://www.mongodb.com/try/download/tools)
* [MongoDB Shell](https://www.mongodb.com/try/download/tools) - this one is not so necessary to download unless users will be accessing the database directly and not through the Python module provided.
* In addition, the [aac_shelter_outcomes.csv](../aac_shelter_outcomes.csv) file will need to be downloaded and you will need to place it in a directory you have made at, C:\data\db

#### MongoImport CSV
After creating C:\data\db and downloading the CSV file, we need to run the Mogno server and import the file to populate the database.  Navigate to C:\Program Files\MongoDB\Server\*MongoVersion*\bin and execute:
```
mongod.exe
```
NOTE: PowerShell users may need to add ".\" to the front of their commands.
After a few minutes, restart the terminal window and navigate back to the same path and test the server is running with:
```
mongo.exe
```
This will launch a version of the mongo shell.  You can use the "show dbs" command to see available databases, and "exit" to return to terminal.  After returning to the terminal, navigate to C:\Program Files\MongoDB\Tools\*MongoVersion*\bin and execute:
```
mongoimport --db=AAC --collection=animals --type=csv --headerline --file=C:\data\db\aac_shelter_outcomes.csv
```
This will import the database documents and make the Mongo server functional locally.

#### Indexing
As this data set is only 10,000 documents, indexing isn't absolutely necessary.  There is very little difference in performance, but I will be writing a blog post (coming soon) and indexing in MongoDB using this collection, if interested in seeing the indexes used on this project.

### [Jupyter](../Jupyter/ProjectTwoDashboard.ipynb)
During the course CS-340, we developed this application using Jupyter Notebook, a programming collaboration software that can be used similarly to an IDE and debugger, with container like properties.  
This project gives you the ability to download the project notebook, run the Jupyter notebook locally, upload the CRUD function file, and play with it for yourself.  As I do not have a ton of experience with this (and, really, the experts explain it best), you can read more about how to do that [here](https://jupyter.readthedocs.io/en/latest/running.html).

## DBMscript
Admins can run DBMscript from the command line: 
In Windows:
```
DBMscript.py
```
In Linux:
```
python3 DBMscript.py
```
To update data, reference the following Python dictionary as a template for the keys available to update in the documents in this collection:
```python
{"age_upon_outcome" : age,
  "animal_id" : ID,
  "animal_type" : animalType,
  "breed" : breed,
  "color" : color,
  "date_of_birth" : DOB,
  "datetime" : "", - uses the Python Date() function to log the date the record was created
  "name" : name,
  "outcome_subtype" : subtype,
  "outcome_type" : outcomeType,
  "sex_upon_outcome" : sex,
  "age_upon_outcome_in_weeks" : ageInWeeks
  }
```
