-- TABLES

CREATE TABLE Users
(email VARCHAR(30) NOT NULL PRIMARY KEY,
name VARCHAR(100) NOT NULL);

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
(u_email VARCHAR(100) NOT NULL,
term VARCHAR(100) NOT NULL,
year INTEGER NOT NULL,
program_name VARCHAR(100) NOT NULL,
PRIMARY KEY (u_email, term, year, program_name),
UNIQUE (u_email, term, year),
FOREIGN KEY (u_email) REFERENCES Users(email),
FOREIGN KEY (program_name) REFERENCES Program(name));

CREATE TABLE Review
(id INTEGER NOT NULL PRIMARY KEY,
abroad_code VARCHAR(100) NOT NULL,
program_name VARCHAR(100) NOT NULL REFERENCES Program(name),
u_email VARCHAR(100) NOT NULL,
content VARCHAR(1000) NOT NULL,
rating FLOAT NOT NULL CHECK (rating >= 0 AND rating <= 5.0),
difficulty FLOAT NOT NULL CHECK (difficulty >= 0 AND difficulty <= 5.0),
anon INTEGER NOT NULL CHECK (anon = 0 OR anon = 1),
UNIQUE(u_email, abroad_code, program_name));

CREATE TABLE Likes
(u_email VARCHAR(100) NOT NULL,
review_id INTEGER NOT NULL,
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
	IF (OLD.program_name <> NEW.program_name AND OLD.u_email = Review.u_email AND OLD.program_name = Review.program_name) FROM Review THEN
	DELETE FROM Review
	WHERE OLD.u_email = Review.u_email AND OLD.program_name = Review.program_name;
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER No_Phantom_Reviews
	AFTER UPDATE OR DELETE ON AbroadUser
	FOR EACH ROW
	EXECUTE PROCEDURE TS_No_phantom();

CREATE FUNCTION TS_No_fake_reviews() RETURNS TRIGGER AS $$
BEGIN
	IF (NEW.program_name NOT IN (SELECT program_name FROM AbroadUser WHERE u_email = NEW.u_email)) THEN
	RAISE EXCEPTION 'Cannot be writing a review for a course in a program you have not been in';
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TS_No_fake_reviews
	BEFORE INSERT ON Review
	FOR EACH ROW EXECUTE PROCEDURE TS_No_fake_reviews();

-- INSERTS

INSERT INTO Users VALUES ('ddc27@duke.edu', 'david');
INSERT INTO Users VALUES('mr328@duke.edu', 'malavi');
INSERT INTO Users VALUES('smw81@duke.edu', 'samantha');
INSERT INTO Users VALUES('al343@duke.edu', 'annie');
INSERT INTO Users VALUES('aaz10@duke.edu', 'abby');
INSERT INTO Users VALUES('aq18@duke.edu', 'alex');

INSERT INTO Program VALUES('Duke in Berlin', 'Germany');
INSERT INTO Program VALUES('Duke in Madrid', 'Spain');
INSERT INTO Program VALUES('University of New South Wales', 'Australia');

INSERT INTO Course VALUES('Duke in Berlin', 'Comp Genomics', '0434-L-982', 'CS', 'CS 260');
INSERT INTO Course VALUES('Duke in Madrid', 'Operating Systems', 'CSSLD-3301', 'CS', 'CS 330');
INSERT INTO Course VALUES('University of New South Wales', 'VLSI', 'ECSDE-3520', 'ECE', 'ECE 350');
INSERT INTO Course VALUES('University of New South Wales', 'Aborigines', 'CLSEQW3520', 'CULANTH', 'CULATNH 400');

INSERT INTO AbroadUser VALUES ('ddc27@duke.edu', 'Spring', 2019, 'Duke in Berlin');
INSERT INTO AbroadUser VALUES ('mr328@duke.edu', 'Fall', 2019, 'Duke in Madrid');
INSERT INTO AbroadUser VALUES ('smw81@duke.edu', 'Spring', 2020, 'University of New South Wales');
INSERT INTO AbroadUser VALUES ('aq18@duke.edu', 'Spring', 2020, 'University of New South Wales');

INSERT INTO Review VALUES (1, '0434-L-982', 'Duke in Berlin', 'ddc27@duke.edu', 'I think this class is amazing!', 4.5, 2.0, 1);
INSERT INTO Review VALUES (2, 'CSSLD-3301', 'Duke in Madrid', 'mr328@duke.edu', 'I think this class SUCKS!', 1, 5, 0);
INSERT INTO Review VALUES (3, 'ECSDE-3520', 'University of New South Wales', 'smw81@duke.edu', 'I think this rocks hehe!', 5, 1, 0);

INSERT INTO Likes VALUES ('aaz10@duke.edu', 1);
INSERT INTO Likes Values ('al343@duke.edu', 3);

-- TESTING TRIGGERS

INSERT INTO Review VALUES(4, '0434-L-982', 'Duke in Berlin', 'aq18@duke.edu', 'HA I did not even take this course', 1, 5, 1);
