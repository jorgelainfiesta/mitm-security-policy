CREATE TABLE "mail" (
    "id_mail" serial NOT NULL PRIMARY KEY,
    "sender" varchar(30) NOT NULL,
    "body" varchar(3000) NOT NULL,
    "recipient" varchar(50) NOT NULL references recipient(id_recipient),
    "tag" varchar(50) NOT NULL references tag(id_tag), 
);


CREATE TABLE "tag" (
    "id_tag" serial NOT NULL PRIMARY KEY,
    "key" varchar(200) NOT NULL,
    "value" varchar(200) NOT NULL
);

CREATE TABLE "recipient" (
    "id_recipient" serial NOT NULL PRIMARY KEY,
    "mail" varchar(30) NOT NULL,
    "tag" varchar(50) NOT NULL references tag(id_tag), 
);

CREATE TABLE "password" (
    "password_id" serial NOT NULL PRIMARY KEY,
    "mail" varchar(30) NOT NULL,
    "password" varchar(50) NOT NULL,
     "tag" varchar(50) NOT NULL references tag(id_tag), 
);

CREATE TABLE "status" (
    "status_id" serial NOT NULL PRIMARY KEY,
    "key" varchar(30) NOT NULL,
    "value" varchar(50) NOT NULL,
    "tag" varchar(50) NOT NULL references tag(id_tag),
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







