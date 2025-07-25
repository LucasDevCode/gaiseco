-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Prompts;
DROP TABLE IF EXISTS Groups;


CREATE TABLE Groups (
  group_id INTEGER PRIMARY KEY AUTOINCREMENT,
  role TEXT NOT NULL,
  description TEXT
);

CREATE TABLE Users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  group_id INTEGER NOT NULL,
  FOREIGN KEY (group_id) REFERENCES Groups (group_id)
);

CREATE TABLE Prompts (
  prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
  employee_ip TEXT NOT NULL,
  model TEXT NOT NULL,
  session TEXT NOT NULL,
  employee_name TEXT NOT NULL,
  prompt TEXT NOT NULL,
  issue TEXT NOT NULL,
  minimum_score FLOAT NOT NULL,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO Groups (role, description)
VALUES ('admin', 'Posição com maior nível de acesso. Somente ele pode registrar novos usuários.');

INSERT INTO Groups (role, description)
VALUES ('manager', 'Gerente responsável por gerenciar a equipe que utilizar os chats.');


INSERT INTO Users (username, email, password, group_id)
VALUES ('admin' , 'admin@admin.com', 'scrypt:32768:8:1$5B4z2PBQgeCRr7Xp$a2d288d0696f19631684df802797e9f75284337b95b257b42ce03c577b307aadf3e96e6595db052978f1989e696b10d158df1ea1bda89315c10667b904da846a', 1);




INSERT INTO Users (username, email, password, group_id)
VALUES ('manager1' , 'gaiseco.server@gmail.com', 'scrypt:32768:8:1$cNtGmr2C6wTCM8Sa$5cf605d153206e03deab4802ad6f984fd96d8ce484f51cd47bccdf73e1b711569c8c1a4bbcf6439042aff5992e3e0929d6796f9d55d6d67b87ef5637aa6c67be', 2);

INSERT INTO Users (username, email, password, group_id)
VALUES ('manager2' , 'gaiseco.server@gmail.com', 'scrypt:32768:8:1$psCfWtJPOPaROUYi$f4f0e7b8eeee451f0e865425ccf55086fdc9af6aa7b7e393bd583de2ef00675c195dcdfd6a25b8342993641f03b1cd301bb4b5fe093df545abcf4cd0cdb65ad1', 2);
