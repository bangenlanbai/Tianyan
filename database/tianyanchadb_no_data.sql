-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: tianyanchadb
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company` (
  `company_id` varchar(20) NOT NULL,
  `company_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mod_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--


--
-- Table structure for table `company_executive`
--

DROP TABLE IF EXISTS `company_executive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_executive` (
    -- 高管信息表
  `id` int NOT NULL AUTO_INCREMENT,
  `company_id` varchar(20) DEFAULT NULL,
  `group_id` int NOT NULL,
  `position` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `report_date` date NOT NULL,
  `mod_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `person_id` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `company_executive_company_person_id_fk` (`person_id`),
  KEY `company_executive_company_company_id_fk` (`company_id`),
  KEY `company_executive_executive_group_group_id_fk` (`group_id`),
  CONSTRAINT `company_executive_company_company_id_fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`),
  CONSTRAINT `company_executive_company_person_id_fk` FOREIGN KEY (`person_id`) REFERENCES `company_person` (`id`),
  CONSTRAINT `company_executive_executive_group_group_id_fk` FOREIGN KEY (`group_id`) REFERENCES `executive_group` (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=187 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_executive`
--

--
-- Table structure for table `company_illegals`
--

DROP TABLE IF EXISTS `company_illegals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_illegals` (
        -- 违规处理表
  `id` varchar(20) NOT NULL,
  `company_id` varchar(20) DEFAULT NULL,
  `disposer` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `default_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `illegal_act_withlink` text,
  `punish_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `punish_explain_withlink` text,
  `punish_object` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `announcement_date` datetime DEFAULT NULL,
  `currency_unit` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `mod_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `company_illegals_company_company_id_fk` (`company_id`),
  CONSTRAINT `company_illegals_company_company_id_fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_illegals`
--

LOCK TABLES `company_illegals` WRITE;
/*!40000 ALTER TABLE `company_illegals` DISABLE KEYS */;
/*!40000 ALTER TABLE `company_illegals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_person`
--

DROP TABLE IF EXISTS `company_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `company_person` (
    -- 公司员工表
  `id` varchar(20) NOT NULL,
  `name` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `age` int DEFAULT NULL,
  `sex` varchar(1) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '男',
  `education` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `resume` text,
  `mod_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_person`
--

--
-- Table structure for table `executive_group`
--

DROP TABLE IF EXISTS `executive_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `executive_group` (
    -- 职位分组
  `group_id` int NOT NULL,
  `group_name` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `executive_group`
--

LOCK TABLES `executive_group` WRITE;
/*!40000 ALTER TABLE `executive_group` DISABLE KEYS */;
INSERT INTO `executive_group` VALUES (1,'董事会'),(2,'监事会'),(3,'高管');
/*!40000 ALTER TABLE `executive_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salary_table`
--

DROP TABLE IF EXISTS `salary_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salary_table` (
    -- 薪资表
  `id` int NOT NULL AUTO_INCREMENT,
  `person_id` varchar(20) NOT NULL,
  `company_id` varchar(20) DEFAULT NULL,
  `money` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `mod_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `numberOfSharesWithUnit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `salary_table_company_company_id_fk` (`company_id`),
  KEY `salary_table_company_person_id_fk` (`person_id`),
  CONSTRAINT `salary_table_company_company_id_fk` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`),
  CONSTRAINT `salary_table_company_person_id_fk` FOREIGN KEY (`person_id`) REFERENCES `company_person` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salary_table`
--

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-14 11:48:17
