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
    question_id                 integer NOT NULL,
    comment_message             character varying NOT NULL,
    comment_submission_time     integer NOT NULL,
    comment_vote_number         integer NOT NULL,
    answer_id                   int PRIMARY KEY,
    CONSTRAINT fk_questions
        FOREIGN  KEY (question_id)
            REFERENCES questions (question_id)
);


    INSERT INTO questions
    VALUES (1, 'Chcę na święta upiec dobry piernik dla 5 osób. Czy ktoś z Was ma jakiś ciekawy przepis dla początkującego kucharza?Pater noster, qui es in caelis, sanctificetur nomen tuum, adveniat regnum tuum, fiat voluntas tua sicut in caelo et in terra.
Panem nostrum quotidianum da nobis hodie;
et dimitte nobis debita nostra, sicut et nos dimittimus debitoribus nostris, et ne nos inducas in tentationem, sed libera nos a malo. Amen.', 1493368154, 'Jak zrobić dobry piernik?', 5, 3),
            (2, 'Cześć. Pierwszy raz zrobiłam dzisiaj świąteczne ciasteczka z przepisu Pani Gessler. Wyszły obłędne, koniecznie musicie ich spróbować.Pater noster, qui es in caelis, sanctificetur nomen tuum, adveniat regnum tuum, fiat voluntas tua sicut in caelo et in terra.
Panem nostrum quotidianum da nobis hodie;
et dimitte nobis debita nostra, sicut et nos dimittimus debitoribus nostris, et ne nos inducas in tentationem, sed libera nos a malo. Amen.',1493368238, 'Przepis na świąteczne ciasteczka.', 8, 7 ),
            (3, 'Szukam pomysłu na to, czym ozdobić świąteczne ciasto. Lukrem, gotowymi ozdobami, czekoladą? I gdzie kupić takie cudeńka? Z góry dzięki za opdowiedź.Pater noster, qui es in caelis, sanctificetur nomen tuum, adveniat regnum tuum, fiat voluntas tua sicut in caelo et in terra.
Panem nostrum quotidianum da nobis hodie;
et dimitte nobis debita nostra, sicut et nos dimittimus debitoribus nostris, et ne nos inducas in tentationem, sed libera nos a malo. Amen.', 1493368678, 'Czym ozdobić ciasto?', 6, 2),
            (4, 'Chciałem na świeta przygotować wypieki dla rodziny, ale popsuł się mój wiekowy mikser. Czy ktoś z Was może polecić jakąś firmę, albo konkrenty model?Pater noster, qui es in caelis, sanctificetur nomen tuum, adveniat regnum tuum, fiat voluntas tua sicut in caelo et in terra.
Panem nostrum quotidianum da nobis hodie;
et dimitte nobis debita nostra, sicut et nos dimittimus debitoribus nostris, et ne nos inducas in tentationem, sed libera nos a malo. Amen.', 1493368234, 'Gdzie kupić mikser?', 7, 9);
