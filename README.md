# Devils Abroad
To build and populate the database with initial values, navigate to milestone2 folder in your VM and paste in:

1) dropdb devils_abroad; createdb devils_abroad; psql devils_abroad -af create.sql

2) cd ..

3) python app.py

In order to run the Flask web application, set up your VM with this repository and run app.py. From the VM, navigate to a web browser and navigate towards http://localhost:5000/
