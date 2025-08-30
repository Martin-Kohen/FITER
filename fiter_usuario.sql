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
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  `Apellido` varchar(255) NOT NULL,
  `Mail` varchar(255) NOT NULL,
  `Contrasenia` varchar(255) NOT NULL,
  `Fecha_de_nacimiento` date DEFAULT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `IdUsuario` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'tobi','inzuz','tobi','juanpene','2006-04-14'),(2,'asda','tobi','asefd','tobi','2025-08-14'),(3,'asdda','asdad','sadasd','ed08c290d7e22f7bb324b15cbadce35b0b348564fd2d5f95752388d86d71bcca','2025-08-13'),(4,'awdad','awdada','dwad','d3b65fd93db07b5d7d9c0a239875ae271b35a13e6fb20b5eafeae599e96a98e1','2025-08-02'),(5,'asdad','adas','asdaa','50ad41624c25e493aa1dc7f4ab32bdc5a3b0b78ecc35b539936e3fea7c565af7','2025-08-07'),(6,'asdsad','adasd','asdasd','2e17b6c1df874c4ef3a295889ba8dd7170bc5620606be9b7c14192c1b3c567aa','2025-07-30'),(7,'asdasdasd','asdad','dasd','2aeb25716a0a859efb6c2607950ee8293e1c25a57259c46db9b60f30858a21fe','2025-08-11'),(8,'adsadad','dasda','dasdsads@gmail.com','2aeb25716a0a859efb6c2607950ee8293e1c25a57259c46db9b60f30858a21fe','2025-07-31'),(9,'asdad','adsad','asdad@saa.ss','2aeb25716a0a859efb6c2607950ee8293e1c25a57259c46db9b60f30858a21fe','2025-08-20');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-29 21:30:38
