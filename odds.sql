CREATE database epl_fixtures,

CREATE TABLE epl_fixtures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT UNIQUE,
    match_date DATETIME,
    home_team VARCHAR(255),
    away_team VARCHAR(255),
    status VARCHAR(50)
);



 'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'odds'