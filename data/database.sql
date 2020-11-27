DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS questions;


CREATE TABLE questions
(
    question_id              int PRIMARY KEY ,
    message         character varying NOT NULL,
    submission_time int NOT NULL,
    title           character varying NOT NULL,
    view_number     int NOT NULL,
    vote_number     int NOT NULL,
    image bytea
);



CREATE TABLE answers
(
    answer_id       int PRIMARY KEY,
    submission_time timestamp without time zone NOT NULL,
    vote_number     integer NOT NULL,
    question_id     integer NOT NULL,
    message         character varying NOT NULL,
    image bytea,
    CONSTRAINT fk_questions
        FOREIGN  KEY (question_id)
            REFERENCES questions (question_id)
);

    INSERT INTO questions
    VALUES (1, 'Why am I here?', 1493368154, 'Why?', 5, 3),
            (2, 'Jaka dzisiaj jest pogoda?',1493368238, 'Pogoda', 8, 7 ),
            (3, 'Co dzisiaj robiłeś?', 1493368678, 'Zabawa', 6, 2),
            (4, 'Co jadłaś na obiad?', 1493368234, 'Kuchnia', 7, 9);

--
--
-- INSERT INTO mentor
-- VALUES (2, 'Bugs', 'Bunny', '+36 (46) 518718', 'bugs.bunny@codecool.com', 'Miskolc', NULL),
--        (3, 'Scooby', 'Doo', '+40 (31) 7309201', 'scooby.doo@codecool.com', 'Bucharest', 7),
--        (4, 'Mickey', 'Mouse', '+40 (31) 7309203', 'mickey.mouse@codecool.com', 'Bucharest', 4),
--        (5, 'Bob', 'Sponge', '+36 (77) 908069', 'bob.sponge@codecool.com', 'Miskolc', 42),
--        (6, 'Homer', 'Simpson', '+48 (88) 4233837', 'homer.simpson@codecool.com', 'Warsaw', 42),
--        (7, 'Donald', 'Duck', '+36 (82) 548410', 'donald.duck@codecool.com', 'Budapest', 13),
--        (8, 'Bart', 'Simpson', '+36 (96) 657514', 'bart.simpson@codecool.com', 'Budapest', 11),
--        (9, 'Tom', 'Cat', '+48 (67) 9656765', 'tom.cat@codecool.com', 'Warsaw', 3),
--        (10, 'Jerry', 'Mouse', '+48 (78) 1620198', 'jerry.mouse@codecool.com', 'Warsaw', 5),
--        (11, 'Daffy', 'Duck', '+48 (78) 7580415', 'daffy.duck@codecool.com.com', 'Warsaw', 90),
--        (12, 'Pink', 'Panther', '+36 (49) 407323', 'pink.panther@codecool.com', 'Budapest', 5),
--        (13, 'Charlie', 'Brown', '+48 (79) 7708347', 'charlie.brown@codecool.com', 'Warsaw', 13),
--        (14, 'Fred', 'Flintstone', '+48 (51) 7112056', 'fred.flintstone@codecool.com', 'Kraków', 8),
--        (15, 'Brian', 'Griffin', '+48 (66) 6396787', 'brian.griffin@codecool.com', 'Kraków', 9),
--        (16, 'Yosemite', 'Sam', '+48 (69) 9945475', 'yosemite.sam@codecool.com', 'Kraków', 3),
--        (17, 'Yogi', 'Bear', '+36 (27) 154667', 'yogi.bear@codecool.com', 'Miskolc', NULL),
--        (18, 'Peter', 'Griffin', '+40 (31) 7309202', 'peter.griffin@codecool.com', 'Bucharest', 55),
--        (19, 'Porky', 'Pig', '+36 (87) 126675', 'porky.pig@codecool.com', 'Miskolc', 55),
--        (20, 'Buzz', 'Lightyear', '+40 (348) 432326', 'buzz.lightyear@codecool.com', 'Bucharest', 3),
--        (21, 'Road', 'Runner', '+40 (264) 414163', 'road.runner@codecool.com', 'Bucharest', 77),
--        (22, 'Lisa', 'Simpson', '+36 (68) 548366', 'lisa.simpson@codecool.com', 'Budapest', 5),
--        (23, 'Scrooge', 'McDuck', '+36 (82) 635078', 'scrooge.mcduck@codecool.com', 'Budapest', NULL),
--        (1, 'Eric', 'Cartman', '+48 (78) 3305247', 'eri.cartman@codecool.com', 'Kraków', 23);
--
-- SELECT pg_catalog.setval('mentor_id_seq', 23, TRUE);
