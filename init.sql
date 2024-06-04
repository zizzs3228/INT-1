CREATE TABLE empty_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    str VARCHAR(255)
);


CREATE TABLE test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    str VARCHAR(255)
);

INSERT INTO test_table (str) VALUES
('test1'),
('test2'),
('Sasha'),
('Masha'),
('bruhmmmm'),
(NULL);


CREATE TABLE break_index1 (
  id int(11) NOT NULL AUTO_INCREMENT,
  str VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (id)
);

INSERT INTO break_index1 (str) VALUES
('test1'),
('test2'),
('Sasha'),
('Masha'),
('bruhmmmm'),
(NULL);

INSERT INTO break_index1 (str) SELECT REPEAT('aaaaaaaaaa', FLOOR(RAND() * 10 + 1))
FROM information_schema.columns
LIMIT 100000;

CREATE TABLE break_index2 (
  id int(11) NOT NULL AUTO_INCREMENT,
  strtext text(255) DEFAULT NULL,
  PRIMARY KEY (id)
);

INSERT INTO break_index2 (strtext) VALUES
('test1'),
('test2'),
('Sasha'),
('Masha'),
('bruhmmmm'),
(NULL);

INSERT INTO break_index2 (strtext) SELECT REPEAT('aaaaaaaaaa', FLOOR(RAND() * 10 + 1))
FROM information_schema.columns
LIMIT 100000;