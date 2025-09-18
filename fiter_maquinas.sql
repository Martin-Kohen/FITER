-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: fiter
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `maquinas`
--

DROP TABLE IF EXISTS `maquinas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maquinas` (
  `idMaquinas` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  `Estado` varchar(255) NOT NULL,
  `idSede` int(11) DEFAULT NULL,
  PRIMARY KEY (`idMaquinas`),
  KEY `fk_maquinas_sedes` (`idSede`),
  CONSTRAINT `fk_maquinas_sedes` FOREIGN KEY (`idSede`) REFERENCES `sedes` (`idSedes`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maquinas`
--

LOCK TABLES `maquinas` WRITE;
/*!40000 ALTER TABLE `maquinas` DISABLE KEYS */;
INSERT INTO `maquinas` VALUES (1,'Cinta de correr','Activa',2),(2,'Bicicleta fija','Activa',2),(3,'Elíptica','Activa',2),(4,'Máquina de pecho','Activa',2),(5,'Máquina de piernas','Activa',2),(6,'Cinta de correr','Activa',3),(7,'Bicicleta fija','Activa',3),(8,'Elíptica','Activa',3),(9,'Máquina de pecho','Activa',3),(10,'Máquina de piernas','Activa',3),(11,'Cinta de correr','Activa',4),(12,'Bicicleta fija','Activa',4),(13,'Elíptica','Activa',4),(14,'Máquina de pecho','Activa',4),(15,'Máquina de piernas','Activa',4),(16,'Cinta de correr','Activa',5),(17,'Bicicleta fija','Activa',5),(18,'Elíptica','Activa',5),(19,'Máquina de pecho','Activa',5),(20,'Máquina de piernas','Activa',5),(21,'Cinta de correr','Activa',6),(22,'Bicicleta fija','Activa',6),(23,'Elíptica','Activa',6),(24,'Máquina de pecho','Activa',6),(25,'Máquina de piernas','Activa',6),(26,'Cinta de correr','Activa',7),(27,'Bicicleta fija','Activa',7),(28,'Elíptica','Activa',7),(29,'Máquina de pecho','Activa',7),(30,'Máquina de piernas','Activa',7),(31,'Cinta de correr','Activa',8),(32,'Bicicleta fija','Activa',8),(33,'Elíptica','Activa',8),(34,'Máquina de pecho','Activa',8),(35,'Máquina de piernas','Activa',8),(36,'Cinta de correr','Activa',9),(37,'Bicicleta fija','Activa',9),(38,'Elíptica','Activa',9),(39,'Máquina de pecho','Activa',9),(40,'Máquina de piernas','Activa',9),(41,'Cinta de correr','Activa',10),(42,'Bicicleta fija','Activa',10),(43,'Elíptica','Activa',10),(44,'Máquina de pecho','Activa',10),(45,'Máquina de piernas','Activa',10),(46,'Cinta de correr','Activa',11),(47,'Bicicleta fija','Activa',11),(48,'Elíptica','Activa',11),(49,'Máquina de pecho','Activa',11),(50,'Máquina de piernas','Activa',11),(51,'Cinta de correr','Activa',12),(52,'Bicicleta fija','Activa',12),(53,'Elíptica','Activa',12),(54,'Máquina de pecho','Activa',12),(55,'Máquina de piernas','Activa',12),(56,'Cinta de correr','Activa',13),(57,'Bicicleta fija','Activa',13),(58,'Elíptica','Activa',13),(59,'Máquina de pecho','Activa',13),(60,'Máquina de piernas','Activa',13),(61,'Cinta de correr','Activa',14),(62,'Bicicleta fija','Activa',14),(63,'Elíptica','Activa',14),(64,'Máquina de pecho','Activa',14),(65,'Máquina de piernas','Activa',14),(66,'Cinta de correr','Activa',15),(67,'Bicicleta fija','Activa',15),(68,'Elíptica','Activa',15),(69,'Máquina de pecho','Activa',15),(70,'Máquina de piernas','Activa',15),(71,'Cinta de correr','Activa',16),(72,'Bicicleta fija','Activa',16),(73,'Elíptica','Activa',16),(74,'Máquina de pecho','Activa',16),(75,'Máquina de piernas','Activa',16),(76,'Cinta de correr','Activa',17),(77,'Bicicleta fija','Activa',17),(78,'Elíptica','Activa',17),(79,'Máquina de pecho','Activa',17),(80,'Máquina de piernas','Activa',17);
/*!40000 ALTER TABLE `maquinas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-18 17:39:42
