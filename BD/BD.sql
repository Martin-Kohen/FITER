-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: fiter
-- ------------------------------------------------------
-- Server version	8.0.43

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
  `idMaquinas` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Estado` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `idSede` int DEFAULT NULL,
  PRIMARY KEY (`idMaquinas`),
  KEY `fk_maquinas_sedes` (`idSede`),
  CONSTRAINT `fk_maquinas_sedes` FOREIGN KEY (`idSede`) REFERENCES `sedes` (`idSedes`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maquinas`
--

LOCK TABLES `maquinas` WRITE;
/*!40000 ALTER TABLE `maquinas` DISABLE KEYS */;
INSERT INTO `maquinas` VALUES (1,'Cinta de correr','Activo',2),(2,'Bicicleta fija','Inactivo',2),(3,'Elíptica','Activo',2),(4,'Máquina de pecho','Activo',2),(5,'Máquina de piernas','Inactivo',2),(6,'Cinta de correr','Activa',3),(7,'Bicicleta fija','Activa',3),(8,'Elíptica','Activa',3),(9,'Máquina de pecho','Activa',3),(10,'Máquina de piernas','Activa',3),(11,'Cinta de correr','Activa',4),(12,'Bicicleta fija','Activa',4),(13,'Elíptica','Activa',4),(14,'Máquina de pecho','Activa',4),(15,'Máquina de piernas','Activa',4),(16,'Cinta de correr','Activa',5),(17,'Bicicleta fija','Activa',5),(18,'Elíptica','Activa',5),(19,'Máquina de pecho','Activa',5),(20,'Máquina de piernas','Activa',5),(21,'Cinta de correr','Activa',6),(22,'Bicicleta fija','Activa',6),(23,'Elíptica','Activa',6),(24,'Máquina de pecho','Activa',6),(25,'Máquina de piernas','Activa',6),(26,'Cinta de correr','Activa',7),(27,'Bicicleta fija','Activa',7),(28,'Elíptica','Activa',7),(29,'Máquina de pecho','Activa',7),(30,'Máquina de piernas','Activa',7),(31,'Cinta de correr','Activa',8),(32,'Bicicleta fija','Activa',8),(33,'Elíptica','Activa',8),(34,'Máquina de pecho','Activa',8),(35,'Máquina de piernas','Activa',8),(36,'Cinta de correr','Activa',9),(37,'Bicicleta fija','Activa',9),(38,'Elíptica','Activa',9),(39,'Máquina de pecho','Activa',9),(40,'Máquina de piernas','Activa',9),(41,'Cinta de correr','Activa',10),(42,'Bicicleta fija','Activa',10),(43,'Elíptica','Activa',10),(44,'Máquina de pecho','Activa',10),(45,'Máquina de piernas','Activa',10),(46,'Cinta de correr','Activa',11),(47,'Bicicleta fija','Activa',11),(48,'Elíptica','Activa',11),(49,'Máquina de pecho','Activa',11),(50,'Máquina de piernas','Activa',11),(51,'Cinta de correr','Activa',12),(52,'Bicicleta fija','Activa',12),(53,'Elíptica','Activa',12),(54,'Máquina de pecho','Activa',12),(55,'Máquina de piernas','Activa',12),(56,'Cinta de correr','Activa',13),(57,'Bicicleta fija','Activa',13),(58,'Elíptica','Activa',13),(59,'Máquina de pecho','Activa',13),(60,'Máquina de piernas','Activa',13),(61,'Cinta de correr','Activa',14),(62,'Bicicleta fija','Activa',14),(63,'Elíptica','Activa',14),(64,'Máquina de pecho','Activa',14),(65,'Máquina de piernas','Activa',14),(66,'Cinta de correr','Activa',15),(67,'Bicicleta fija','Activa',15),(68,'Elíptica','Activa',15),(69,'Máquina de pecho','Activa',15),(70,'Máquina de piernas','Activa',15),(71,'Cinta de correr','Activa',16),(72,'Bicicleta fija','Activa',16),(73,'Elíptica','Activa',16),(74,'Máquina de pecho','Activa',16),(75,'Máquina de piernas','Activa',16),(76,'Cinta de correr','Activa',17),(77,'Bicicleta fija','Activa',17),(78,'Elíptica','Activa',17),(79,'Máquina de pecho','Activa',17),(80,'Máquina de piernas','Activa',17),(81,'cinta de correr','Activa',18),(82,'cinta de correr','Activa',18),(83,'Jalon al pecho','Activa',18),(84,'Elíptica','Activa',18),(85,'Press banca','Activa',18);
/*!40000 ALTER TABLE `maquinas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sedes`
--

DROP TABLE IF EXISTS `sedes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sedes` (
  `idSedes` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Ubicacion` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `cant_Maquinas` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`idSedes`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sedes`
--

LOCK TABLES `sedes` WRITE;
/*!40000 ALTER TABLE `sedes` DISABLE KEYS */;
INSERT INTO `sedes` VALUES (2,'Abasto','Av. Corrientes 3234, CABA','75'),(3,'Adrogué','Seguí 675, Buenos Aires','112'),(4,'Almagro','Castro Barros 148, CABA','98'),(5,'Almagro 2','Av. Medrano 976, CABA.','64'),(6,'Barrio Norte','Mansilla 2929, CABA','133'),(7,'Caballito','Rosario 744, CABA','89'),(8,'Caballito 2','Av. Acoyte 54, CABA','105'),(9,'Caballito 3','Av. Rivadavia 4475','77'),(10,'Center','Florida 770, Caba','142'),(11,'Cid Campeador','Franklin 710, CABA','51'),(12,'Congreso','Pasco 48, CABA','91'),(13,'Flores','Lautaro 71, CABA','120'),(14,'Hollywood','Humboldt 1575, CABA','101'),(15,'Lomas','Av. Meeks 250','58'),(16,'Microcentro','Lavalle 828, CABA','118'),(17,'Núñez','Miguel B. Sánchez 1013, CABA (Av. Del Libertador al 7500)','149'),(18,'Palermo','Humboldt 2439, CABA','83');
/*!40000 ALTER TABLE `sedes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Apellido` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Mail` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Contrasenia` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Fecha_de_nacimiento` date DEFAULT NULL,
  `Rol` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `logueado` tinyint(1) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `IdUsuario` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'awdaa','awd','awda@wda.com','38816a4bbe78aa3dbff468dc0d08c217df8cc3b4f3c3fd9f139bab84d69dff5c','2025-09-18','Empleado',0),(2,'juan','ojeda','juan@gmail.com','ed08c290d7e22f7bb324b15cbadce35b0b348564fd2d5f95752388d86d71bcca','2025-09-10','Empleado',0),(3,'soyjuanysoygay','inzunza','tobi@gmail.com','cd6f33ab869d39460147064d5c5a72f182f7bb9502ed73f8e239a5a62ff69d42','2025-09-16','Gerente',0),(4,'juan','juan','juan1@gmail.com','ed08c290d7e22f7bb324b15cbadce35b0b348564fd2d5f95752388d86d71bcca','2025-09-17','Gerente',0),(5,'tt','t','tobia@gmail.com','e3b98a4da31a127d4bde6e43033f66ba274cab0eb7eb1c70ec41402bf6273dd8','2025-09-16','Gerente',1),(6,'juangay','t','juan11@gmail.com','189f40034be7a199f1fa9891668ee3ab6049f82d38c68be70f596eab2e1857b7','2025-09-09','Empleado',0),(7,'juan','ojeda','juanfrancoob@gmail.com','b375e3aee4b0869fdee9e7fb8f39975f1ce0c22820d9e87c80676c74f68622e8','2007-01-09','Gerente',1);
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

-- Dump completed on 2025-09-23 16:44:18
