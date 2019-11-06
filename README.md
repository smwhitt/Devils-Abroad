# Devils Abroad - David

11/05/2019: I have converted a semi-comprehensive list of 2775 people who have previously gone abroad to an Excel file (Past_Abroad_Students.xlsl) and to 3 .csv files
which you are free to insert into our databse.
To insert the "Populate Users/Program/AbroadUsers.csv" into the database, first build it and then access the database via psql devils_abroad and type:

COPY Users(email,name,major,grad_year) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Populate Users.csv' DELIMITER ',' CSV HEADER;

http://www.postgresqltutorial.com/import-csv-file-into-posgresql-table/

The columns of the .csv file has to exactly match the order of whatever Table you're trying to insert, but not all attributes of a Table have to be filled out
(as long the variable doesn't have a NOT NULL attribute).