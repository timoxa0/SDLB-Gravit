CREATE USER 'launchserver'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE db;
GRANT ALL PRIVILEGES ON db . * TO 'launchserver'@'localhost';
FLUSH PRIVILEGES;

USE db;

CREATE TABLE `users` (
  `id` varchar(255) NOT NULL,
  `username` varchar(255) UNIQUE DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `uuid` char(36) UNIQUE DEFAULT NULL,
  `accessToken` char(32) DEFAULT NULL,
  `serverID` varchar(41) DEFAULT NULL,
  `hwidId` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
);

DELIMITER //
CREATE TRIGGER setUUID BEFORE INSERT ON users
FOR EACH ROW BEGIN
IF NEW.uuid IS NULL THEN
SET NEW.uuid = UUID();
END IF;
END; //
DELIMITER ;

UPDATE users SET uuid=(SELECT UUID()) WHERE uuid IS NULL;

CREATE TABLE `hwids` (
`id` bigint(20) NOT NULL,
`publickey` blob,
`hwDiskId` varchar(255) DEFAULT NULL,
`baseboardSerialNumber` varchar(255) DEFAULT NULL,
`graphicCard` varchar(255) DEFAULT NULL,
`displayId` blob,
`bitness` int(11) DEFAULT NULL,
`totalMemory` bigint(20) DEFAULT NULL,
`logicalProcessors` int(11) DEFAULT NULL,
`physicalProcessors` int(11) DEFAULT NULL,
`processorMaxFreq` bigint(11) DEFAULT NULL,
`battery` tinyint(1) NOT NULL DEFAULT "0",
`banned` tinyint(1) NOT NULL DEFAULT "0"
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE `hwids`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `publickey` (`publickey`(255));
ALTER TABLE `hwids`
MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
ALTER TABLE `users`
ADD CONSTRAINT `users_hwidfk` FOREIGN KEY (`hwidId`) REFERENCES `hwids` (`id`);