--  to search for all courses in Australia:
SELECT * 
FROM course, program 
WHERE course.program_name = program.name 
AND program.country = 'Australia';

--  to search for all courses in England:

SELECT * 
FROM course, program 
WHERE course.program_name = program.name 
AND program.country = 'Spain';

-- Query to search for all courses in Germany:

SELECT * 
FROM course, program 
WHERE course.program_name = program.name 
AND program.country = 'Germany';

-- Query to search for all courses for University of New South Wales:

SELECT * 
FROM course
WHERE program_name = 'University of New South Wales';

-- Query to search for all courses for Duke in Berlin:

SELECT * 
FROM course
WHERE program_name = 'Duke In Berlin';

-- Query to search for all courses for Duke in Madrid:

SELECT * 
FROM course
WHERE program_name = 'Duke In Madrid';

-- Query to search for the average rating from all reviews based on difficulty:

SELECT AVG(rating)
FROM review
GROUP BY difficulty;

-- Query to search for the average difficulty at Duke in Geneva:

SELECT AVG(difficulty)
FROM review
WHERE program_name = 'University of New South Wales';

-- Query to search for the review content given a review ID of '4':

SELECT review.content
FROM review
WHERE review.id = '2';

-- Query to search for all reviews in Duke in Venice;

SELECT review.content
FROM review
WHERE review.program_name = 'Duke in Berlin';

-- Query to search for all people who have studied abroad in Russia

SELECT Users.name 
FROM AbroadUser, Users 
WHERE program_name = 'Duke in Madrid'
AND AbroadUser.u_email = Users.email;

-- Query to search for all people who have studied abroad with emails

SELECT Users.name, AbroadUser.u_email
FROM AbroadUser, Users
WHERE AbroadUser.u_email = Users.email;
