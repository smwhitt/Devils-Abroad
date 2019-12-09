-- TABLES

CREATE TABLE Country
(country_name VARCHAR(50) NOT NULL PRIMARY KEY,
c_id VARCHAR(2) NOT NULL);

CREATE TABLE MajorCodes
(duke_major_code VARCHAR(100) NOT NULL PRIMARY KEY);

CREATE TABLE Program
(program_name VARCHAR(100) NOT NULL PRIMARY KEY,
country VARCHAR(50) NOT NULL);

CREATE TABLE Users
(email VARCHAR(100) NOT NULL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
major VARCHAR(50) NOT NULL,
term VARCHAR(100) NOT NULL,
program_name VARCHAR(100) NOT NULL,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
FOREIGN KEY (program_name) REFERENCES Program(program_name));

CREATE TABLE Contact
(email VARCHAR(100) NOT NULL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
major VARCHAR(50) NOT NULL,
term VARCHAR(100) NOT NULL,
program VARCHAR(100) NOT NULL);

CREATE TABLE Course
(duke_code VARCHAR(100) NOT NULL,
course_name VARCHAR(100) NOT NULL,
program_name VARCHAR(100) NOT NULL,
PRIMARY KEY (program_name, duke_code, course_name),
FOREIGN KEY (program_name) REFERENCES Program(program_name));

--CREATE TABLE AbroadUser
--(u_email VARCHAR(100) NOT NULL,
--term VARCHAR(100) NOT NULL,
--program_name VARCHAR(100) NOT NULL,
--PRIMARY KEY (u_email, term, program_name),
--UNIQUE (u_email, term),
--FOREIGN KEY (u_email) REFERENCES Users(email),
--FOREIGN KEY (program_name) REFERENCES Program(program_name));

-- CREATE TABLE Review
-- (id VARCHAR(100)  NOT NULL PRIMARY KEY,
-- country VARCHAR(100) NOT NULL, --fix later, doesn't reference countries!
-- program_name VARCHAR(100) NOT NULL REFERENCES Program(program_name),
-- duke_code VARCHAR(100) NOT NULL,
-- course_name VARCHAR(100) NOT NULL,
-- u_email VARCHAR(100) NOT NULL,
-- content VARCHAR(1000) NOT NULL,
-- rating FLOAT NOT NULL CHECK (rating >= 0 AND rating <= 5.0),
-- difficulty FLOAT NOT NULL CHECK (difficulty >= 0 AND difficulty <= 5.0),
-- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- UNIQUE(u_email, program_name, duke_code, course_name));

CREATE TABLE Review
(id VARCHAR(100)  NOT NULL PRIMARY KEY,
country VARCHAR(100) NOT NULL, --fix later, doesn't reference countries!
program_name VARCHAR(100) NOT NULL REFERENCES Program(program_name),
duke_major_code VARCHAR(100) NOT NULL REFERENCES MajorCodes(duke_major_code),
duke_code VARCHAR(100) NOT NULL,
course_name VARCHAR(100) NOT NULL,
u_email VARCHAR(100) NOT NULL,
content VARCHAR(1000) NOT NULL,
rating FLOAT NOT NULL CHECK (rating >= 0 AND rating <= 5.0),
difficulty FLOAT NOT NULL CHECK (difficulty >= 0 AND difficulty <= 5.0),
-- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
UNIQUE(u_email, program_name, course_name, duke_code));

CREATE TABLE Likes
(u_email VARCHAR(100) NOT NULL,
review_id VARCHAR(100) NOT NULL,
PRIMARY KEY (u_email, review_id),
FOREIGN KEY (u_email) REFERENCES Users(email),
FOREIGN KEY (review_id) REFERENCES Review(id) ON DELETE CASCADE);


-- TRIGGERS

CREATE FUNCTION TS_No_edit_own_review() RETURNS TRIGGER AS $$ 
BEGIN
	IF (NEW.u_email <> Review.u_email) FROM Review THEN
		RAISE EXCEPTION 'Cannot update or delete reviews that you didn’t write';
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Edit_Own_Review
	BEFORE UPDATE OR DELETE ON Review
	FOR EACH ROW
	EXECUTE PROCEDURE TS_No_edit_own_review();

CREATE FUNCTION TS_No_phantom() RETURNS TRIGGER AS $$
BEGIN
	IF (OLD.program_name <> NEW.program_name AND OLD.email = Review.u_email AND OLD.program_name = Review.program_name) FROM Review THEN
	DELETE FROM Review
	WHERE OLD.u_email = Review.u_email AND OLD.program_name = Review.program_name;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER No_Phantom_Reviews
	AFTER UPDATE OR DELETE ON Users
	FOR EACH ROW
	EXECUTE PROCEDURE TS_No_phantom();

--CREATE FUNCTION TS_No_fake_reviews() RETURNS TRIGGER AS $$
--BEGIN
--	IF (NEW.program_name NOT IN (SELECT program_name FROM Users WHERE email = NEW.u_email)) THEN
--	RAISE EXCEPTION 'Cannot be writing a review for a course in a program you have not been in';
--	END IF;
--	RETURN NEW;
--END;
--$$ LANGUAGE plpgsql;

--CREATE TRIGGER TS_No_fake_reviews
--	BEFORE INSERT ON Review
--	FOR EACH ROW EXECUTE PROCEDURE TS_No_fake_reviews();

-- Indexes

CREATE INDEX Get_User
on Users (email, name);

-- INSERTS
--IMPORTANT NOTE: ORDER OF POPULATING DATABASE IS COUNTRY, PROGRAM, USERS, MAJOR CODE, COURSE, REVIEW
-- Copying the .csv files into the database:::
COPY Country(country_name,c_id) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Countries.csv' DELIMITER ',' CSV HEADER;
COPY Program(program_name,country) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Populate Program.csv' DELIMITER ',' CSV HEADER;
COPY Contact(email,name,major,term,program) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Populate Contact.csv' DELIMITER ',' CSV HEADER;
COPY MajorCodes(duke_major_code) FROM '/home/davidchen1337/devils_abroad/Devils-Abroad/milestone2/Populate MajorCodes.csv' DELIMITER ',' CSV HEADER;

INSERT INTO Users VALUES('smw81@duke.edu', 'Samantha Whitt', 'Computer Science', 'Spring 2020', 'University of New South Wales', 'smwhitt99', '1234');
INSERT INTO Users VALUES('ddc27@duke.edu', 'David Chen', 'Biology', 'Fall 2019', 'Duke in Berlin', 'ddc27', '1234');
INSERT INTO Users VALUES('mr328@duke.edu', 'Malavi Ravindran', 'Computer Science', 'Spring 2018', 'Duke in Madrid', 'mr328', '1234');
INSERT INTO Users VALUES('aq18@duke.edu', 'Alex Qiao', 'Computer Science', 'Spring 2020', 'University of New South Wales', 'aq18', '1234');

INSERT INTO Course VALUES('COMPSCI 330', 'Design and Analysis of Algorithms', 'Duke in Berlin');
INSERT INTO Course VALUES('COMPSCI 300', 'Analysis of Big Data', 'Duke in Madrid');
INSERT INTO Course VALUES('COMPSCI 250', 'Computer Architecture', 'University of New South Wales');
INSERT INTO Course VALUES('COMPSCI 300', 'Networks', 'University of New South Wales');

INSERT INTO Review VALUES('IDfake', 'Australia', 'University of New South Wales', 'COMPSCI', 'COMPSCI 300', 'Networks', 'smw81@duke.edu', 'amazing!', 5, 3);

INSERT INTO Review VALUES ('1', 'Germany', 'Duke in Berlin', 'COMPSCI', 'CS 330', 'Design and Analysis of Algorithms' , 'ddc27@duke.edu', 'I think this class is amazing!', 4, 2);
INSERT INTO Review VALUES ('2', 'Spain', 'Duke in Madrid', 'COMPSCI', 'CS 300', 'Networks', 'mr328@duke.edu', 'I think this class SUCKS!', 1, 5);
INSERT INTO Review VALUES ('3', 'Australia','University of New South Wales', 'COMPSCI', 'CS 250', 'Computer Architecture', 'smw81@duke.edu', 'I think this rocks hehe!', 5, 1);

INSERT INTO Likes VALUES ('ddc27@duke.edu', '2');
INSERT INTO Likes Values ('aq18@duke.edu', '3');

-- TESTING TRIGGERS

-- INSERT INTO Review VALUES ("4", 'Duke in Madrid', 'CS 300', 'Networks' , 'ddc27@duke.edu', 'hahaha i didn’t even take this class!', 4.5, 2.0);
