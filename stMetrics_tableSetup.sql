Create Table: CREATE TABLE `results` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server` varchar(40) DEFAULT NULL,
  `url` varchar(120) DEFAULT NULL,
  `dl` decimal(17,8) DEFAULT NULL,
  `ul` decimal(17,8) DEFAULT NULL,
  `ping` decimal(7,3) DEFAULT NULL,
  `lat` decimal(7,4) DEFAULT NULL,
  `lon` decimal(7,4) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85650 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
