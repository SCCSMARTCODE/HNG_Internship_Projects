-- This will help us set up the database

CREATE DATABASE IF NOT EXISTS `hng_stage2_project_db`;
CREATE USER IF NOT EXISTS `hng_db_user`@localhost IDENTIFIED BY '246c4fb2a74a5571b749191853aeb801';
GRANT ALL PRIVILEGES ON hng_stage2_project_db.* TO 'hng_db_user'@'localhost';
FLUSH PRIVILEGES;
