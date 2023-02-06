drop database team_a;
create database team_a;

\c team_a

CREATE TABLE USERS (
	userid INT,	
	username VARCHAR(15) NOT NULL,
	pswd VARCHAR(30) NOT NULL, 
	fname VARCHAR(15) NOT NULL,
	lname VARCHAR(15) NOT NULL UNIQUE,
	phonenumber VARCHAR(10) UNIQUE,
    email VARCHAR(30) UNIQUE default 'default',
	PRIMARY KEY (userid)
);

CREATE TABLE QUESTIONS (
    userid int,
	qid INT,	
    answer varchar(30) not null,
	hint varchar(100) not null,
	PRIMARY KEY (userid, qid),
    FOREIGN KEY (userid) REFERENCES USERS(userid)  
);

CREATE TABLE CUST_OTP (
    userid int,
    otp varchar(6) not null,
    PRIMARY KEY(userid),
    FOREIGN KEY (userid) REFERENCES USERS(userid)
);
