-- Query to search for all courses for University of New South Wales:

SELECT * 
FROM Course
WHERE program_name = 'University of New South Wales';

-- Query to search for all courses for Duke in Berlin:

SELECT * 
FROM Course
WHERE program_name = 'Duke In Berlin';

-- Query to search for all courses for Duke in Madrid:

SELECT * 
FROM Course
WHERE program_name = 'Duke In Madrid';

-- Query to search for the average rating from all reviews based on difficulty:

SELECT AVG(rating)
FROM Review
GROUP BY difficulty;

-- Query to search for the average difficulty at UNSW:

SELECT AVG(difficulty)
FROM Review
WHERE program_name = 'University of New South Wales';

-- Query to search for the review content given a review ID of '2':

SELECT content
FROM Review
WHERE review.id = '2';

-- Query to search for all reviews in Duke in Berlin;

SELECT content
FROM Review
WHERE review.program_name = 'Duke in Berlin';

-- Query to search for all people who have studied abroad in Madrid

SELECT name 
FROM AbroadUser, Users 
WHERE program_name = 'Duke in Madrid'
AND AbroadUser.u_email = Users.email;

-- Query to search for all people who have studied abroad (with emails)

SELECT Users.name, AbroadUser.u_email
FROM AbroadUser, Users
WHERE AbroadUser.u_email = Users.email;
