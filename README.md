# Devils Abroad
To populate the database with those files, first build it:

dropdb devils_abroad; createdb devils_abroad; psql devils_abroad -af create.sql

Then access the database (psql devils_abroad) and type (replace /home/davidchen1337/devils_abroad with your own directory):

COPY Country(country_name,c_id) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Countries.csv' DELIMITER ',' CSV HEADER; COPY Program(program_name,country) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Populate Program.csv' DELIMITER ',' CSV HEADER; COPY Contact(email,name,major,term,program) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Populate Contact.csv' DELIMITER ',' CSV HEADER; COPY MajorCodes(duke_major_code) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Populate MajorCodes.csv' DELIMITER ',' CSV HEADER;

http://www.postgresqltutorial.com/import-csv-file-into-posgresql-table/

The columns of the .csv file has to exactly match the order of whatever Table you're trying to insert, but not all attributes of a Table have to be filled out (as long the variable doesn't have a NOT NULL attribute).

In order to run the Flask web application, set up your VM with this repository and run app.py. From the VM, navigate to a web browser and navigate towards http://localhost:5000/. 
