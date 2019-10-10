For our project, we will be using postgreSQL (pSQL) to write/create our own databases. We created our own database called "devils_abroad" using the following code provided in class:

dropdb devils_abroad; createdb devils_abroad; psql devils_abroad -af create.sql

In order to load the database, each team member needs to run that command and can visualize it using the command as seen below. For our website, we map the database to python objects by python's API called psycopg2 to better accomodate for future flexibility of the program. We additionally plan on inserting our own information not only using create.sql, but also from a future study abroad survery in the future.

psql devils_abroad -af test-sample.sql > test-sample.out
