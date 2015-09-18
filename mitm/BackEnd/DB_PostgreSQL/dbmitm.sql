CREATE TABLE  mail (
    id_mail INTEGER PRIMARY KEY NOT NULL,
    sender VARCHAR(30) NOT NULL,
    body TEXT NOT NULL,
    recipients TEXT [] NOT NULL references recipient(id_recipient),
    tags TEXT[] NOT NULL references tag(id_tag), 
);


CREATE TABLE tag (
   	id_tag INTEGER PRIMARY KEY NOT NULL,
    key  VARCHAR(200) NOT NULL,
    value VARCHAR(200) NOT NULL
);

CREATE TABLE recipient (
    id_recipient INTEGER PRIMARY KEY NOT NULL,
    mail TEXT  NOT NULL,
    tags TEXT[] NOT NULL references tag(id_tag), 
);

CREATE TABLE password (
    password_id INTEGER PRIMARY KEY NOT NULL,
    mail VARCHAR(30) NOT NULL,
    password VARCHAR(50) NOT NULL,
    tags TEXT[] NOT NULL references tag(id_tag),  
);

CREATE TABLE status (
    status_id INTEGER PRIMARY KEY NOT NULL,
    key varchar(30) NOT NULL,
    value varchar(50) NOT NULL,
    tag varchar(30) NOT NULL references tag(id_tag),
);

CREATE FUNCTION check_password(uname TEXT, pass TEXT)
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
BEGIN
        SELECT  (pwd = $2) INTO passed
        FROM    pwds
        WHERE   username = $1;

        RETURN passed;
END;
$$  LANGUAGE plpgsql
    SECURITY DEFINER
    -- Set a secure search_path: trusted schema(s), then 'pg_temp'.
    SET search_path = admin, pg_temp;



CREATE FUNCTION set_tag(body_text varchar(5000))
	RETURNS TABLE( id int, tag text, value text) AS
$$
SELECT id, tag, value
FROM tag
WHERE tag like $1;
$$
LANGUAGE 'sql' STABLE;







