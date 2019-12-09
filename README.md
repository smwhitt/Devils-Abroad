# Devils Abroad
To populate the database with the .csv files, navigate to the milestone2 folder and edit create.sql lines 78-81 to
replace /home/davidchen1337/devils_abroad/.../Populate [whatever].csv with your own directory

Then enter this:
dropdb devils_abroad; createdb devils_abroad; psql devils_abroad -af create.sql

In order to run the Flask web application, set up your VM with this repository and run app.py. From the VM, navigate to a web browser and navigate towards http://localhost:5000/.
