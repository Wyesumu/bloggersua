-- MySQL dump 10.13  Distrib 8.0.21, for Linux (x86_64)
--
-- Host: localhost    Database: bloggers
-- ------------------------------------------------------
-- Server version	8.0.21-0ubuntu0.20.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blogger`
--

DROP TABLE IF EXISTS `blogger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blogger` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(190) DEFAULT NULL,
  `details` text,
  `img` text,
  `instagram_link` text,
  `youtube_link` text,
  `tiktok_link` text,
  `likee_link` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blogger`
--

LOCK TABLES `blogger` WRITE;
/*!40000 ALTER TABLE `blogger` DISABLE KEYS */;
INSERT INTO `blogger` VALUES (1,'Имя блогера','Описание блогера, информация информация информация информация информация информация информация информация информация информация информация информация ','214143287963356922512908867093810126671.jpg','1','1','',''),(2,'Имя','Описание блогера, информация информация информация информация информация информация информация информация информация информация информация информация','241297717926509945088738481580078484864.jpg','1','','1','1'),(3,'Имя блогера','Описание блогера, информация информация информация информация информация информация информация информация информация информация информация информация','114507703596789412989006977739620011617.jpg','1','','',''),(4,'Имя блогера','Описание блогера, информация информация информация информация информация информация информация информация информация информация информация информация','223652541202902271235091930540745268410.jpg','','1','1','');
/*!40000 ALTER TABLE `blogger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employers`
--

DROP TABLE IF EXISTS `employers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` varchar(190) DEFAULT NULL,
  `name_uk` varchar(190) DEFAULT NULL,
  `name_ru` varchar(190) DEFAULT NULL,
  `name_en` varchar(190) DEFAULT NULL,
  `position_uk` varchar(190) DEFAULT NULL,
  `position_ru` varchar(190) DEFAULT NULL,
  `position_en` varchar(190) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employers`
--

LOCK TABLES `employers` WRITE;
/*!40000 ALTER TABLE `employers` DISABLE KEYS */;
INSERT INTO `employers` VALUES (2,'122889740272657485501463629365375593192.jpg','Галущак Евген Володимирович','Галущак Евгений Владимирович','Galushak Evgeniy Vladimirovich','Голова Асоціації','Глава Ассоциации ','Chairman of the Association'),(3,'61215071289786873247100254899712161309.jpg','Сурков Віталій Константинович','Сурков Виталий Константинович','Surkov Vitaliy Konstantinovich','Секретар Асоціації','Секретарь Ассоциации','Secretary of the Association'),(4,'111065732139631899712182067972371911889.jpg','Єнько Марина Валеріївна','Енько Марина Валерьевна','Yen\'ko Marina Valer\'evna','Член правління','Член правления','Member of the Board'),(5,'83127599040796483026384309571306124372.jpg','Рисак Марія Ігорівна','Рысак Мария Игоревна','Rysak Mariya Igorevna','Член правління','Член правления','Member of the Board'),(6,'154404316826826758665322011389606597712.jpg','Мадяр Анастасія Василівна','Мадяр Анастасия Васильевна','Madyar Anastasiya Vasil\'evna','Головний юрист','Главный юрист','Chief lawyer'),(7,'260229961507481292686294059407184017787.jpg','Іванова Анна Олегівна','Иванова Анна Олеговна ','Ivanova Anna Olegivna','Юрист','Юрист','Lawyer');
/*!40000 ALTER TABLE `employers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gallery`
--

DROP TABLE IF EXISTS `gallery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gallery` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `details` varchar(128) DEFAULT NULL,
  `video` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gallery`
--

LOCK TABLES `gallery` WRITE;
/*!40000 ALTER TABLE `gallery` DISABLE KEYS */;
INSERT INTO `gallery` VALUES (1,'photo1',NULL,''),(2,'photo2',NULL,''),(3,'2 photos',NULL,''),(4,'test',NULL,'');
/*!40000 ALTER TABLE `gallery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gallery__image`
--

DROP TABLE IF EXISTS `gallery__image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gallery__image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gallery_id` int DEFAULT NULL,
  `file_name` text,
  PRIMARY KEY (`id`),
  KEY `gallery_id` (`gallery_id`),
  CONSTRAINT `gallery__image_ibfk_1` FOREIGN KEY (`gallery_id`) REFERENCES `gallery` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gallery__image`
--

LOCK TABLES `gallery__image` WRITE;
/*!40000 ALTER TABLE `gallery__image` DISABLE KEYS */;
INSERT INTO `gallery__image` VALUES (1,1,'13711157787499133842582570356197774015.jpg'),(2,2,'19990081444174391557538890190478818724.jpg'),(3,3,'68082586446347208520363982448393447862.jpg'),(4,3,'50140377024928276848288832003899003061.jpg'),(6,4,'174490135121335274098689238613222535197.jpg');
/*!40000 ALTER TABLE `gallery__image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(190) DEFAULT NULL,
  `surname` varchar(190) DEFAULT NULL,
  `link` varchar(190) DEFAULT NULL,
  `city` varchar(190) DEFAULT NULL,
  `phone` varchar(190) DEFAULT NULL,
  `email` varchar(190) DEFAULT NULL,
  `photo` varchar(190) DEFAULT NULL,
  `statement` varchar(190) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (1,'name','surname','link','Kyiv','+380 123 132 132','132@132.132','262239833156740508241951393605123803865.jpg','205765216379324306335519410405865439467.jpg'),(2,'','','','','','','80953089746847319943682211033583659489.jpg','266236007917696385983653041808517898772.jpg');
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setting`
--

DROP TABLE IF EXISTS `setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `setting` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `value` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setting`
--

LOCK TABLES `setting` WRITE;
/*!40000 ALTER TABLE `setting` DISABLE KEYS */;
INSERT INTO `setting` VALUES (1,'title','Асоціація Блогерів України'),(2,'phone','+380 222 11 11'),(3,'email','AssociateBloggersUa@gmail.com'),(4,'fax','+380 222 11 11'),(5,'address','Киев, ул. Центральная 2'),(6,'instagram','uabloggers.association'),(7,'telegram','UaBloggersUa'),(8,'facebook','uabloggers.association'),(9,'youtube','uabloggers.association');
/*!40000 ALTER TABLE `setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `slider`
--

DROP TABLE IF EXISTS `slider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `slider` (
  `id` int NOT NULL AUTO_INCREMENT,
  `img` text,
  `title` varchar(80) DEFAULT NULL,
  `text` text,
  `dark` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slider`
--

LOCK TABLES `slider` WRITE;
/*!40000 ALTER TABLE `slider` DISABLE KEYS */;
INSERT INTO `slider` VALUES (2,'106773323694317433047725891195182837418.jpg','Welcome to Canvas','Create just what you need for your Perfect Website. Choose from a wide range of Elements &amp; simply put them on your own Canvas.',0),(3,'223813007536143481835330809978135280132.jpg','Title','Create just what you need for your Perfect Website. Choose from a wide range of Elements &amp; simply put them on your own Canvas.',1),(4,'261398651614484192834165537417611252421.jpg','Title','Create just what you need for your Perfect Website. Choose from a wide range of Elements &amp; simply put them on your own Canvas.',1);
/*!40000 ALTER TABLE `slider` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-17 10:17:17
