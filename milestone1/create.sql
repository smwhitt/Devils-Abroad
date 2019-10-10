CREATE TABLE User
(email VARCHAR(30) NOT NULL PRIMARY KEY,
name VARCHAR(100) NOT NULL
CONSTRAINT Only_Duke_Emails CHECK (SELECT SUBSTRING (email, LEN(email) - 8, LEN(email) = ‘duke.edu’));

CREATE TABLE Program
(name VARCHAR(100) NOT NULL PRIMARY KEY,
country VARCHAR(50) NOT NULL);
 

CREATE TABLE Course
(program_name VARCHAR(100) NOT NULL ,
abroad_course_name VARCHAR(100) NOT NULL,
abroad_code VARCHAR (100) NOT NULL,
duke_major_code VARCHAR (100) NOT NULL,
duke_code VARCHAR (100) NOT NULL,
PRIMARY KEY (program_name, abroad_code),
FOREIGN KEY (program_name) REFERENCES Program(name));


CREATE TABLE AbroadUser
(user_email VARCHAR(100) NOT NULL,
term VARCHAR(100) NOT NULL,
year INTEGER NOT NULL,
program_name VARCHAR(100) NOT NULL,
PRIMARY KEY (user_email, term, year, program_name),
UNIQUE (user_email, term, year),
FOREIGN KEY (user_email) REFERENCES User(email),
FOREIGN KEY (program_name) REFERENCES Program(name));


CREATE TABLE Review
(id INTEGER NOT NULL PRIMARY KEY,
abroad_code VARCHAR(100) NOT NULL,
program_name VARCHAR(100) NOT NULL REFERENCES Program(name),
user_email VARCHAR(100) NOT NULL REFERENCES AbroadUser(user_email),
content VARCHAR(1000) NOT NULL,
rating FLOAT NOT NULL CHECK (rating > 0 AND rating < 5.0),
difficulty FLOAT NOT NULL CHECK (difficulty > 0 AND difficulty < 5.0),
anon INTEGER NOT NULL CHECK (anon = 0 OR anon = 1),
UNIQUE(user_email, abroad_code, program_name));

CREATE TABLE Likes
(user_email VARCHAR(100) NOT NULL,
review_id INTEGER NOT NULL,
PRIMARY KEY (user_email, review_id),
FOREIGN KEY (user_email) REFERENCES User(email),
FOREIGN KEY (review_id) REFERENCES Review(id) ON DELETE CASCADE);
