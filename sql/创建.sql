SELECT * FROM user;
INSERT INTO user(futures_account, futures_password,tq_account,tq_password,account_type,disable) VALUES('182','111','996dev','12',1,0);
INSERT INTO user(futures_account, futures_password,tq_account,tq_password,account_type,disable) VALUES('182','111','996dev','12',1,0);


UPDATE user SET tq_password = '18' WHERE id = 1;
DELETE FROM user WHERE id = 2;
DELETE FROM user;

DROP TABLE test.user;

ALTER TABLE user ADD COLUMN disable INT NOT NULL DELETE(0);