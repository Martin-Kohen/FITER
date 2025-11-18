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
-- Table structure for table `actividades`
--

DROP TABLE IF EXISTS `actividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actividades` (
  `ID_Actividad` int(8) NOT NULL,
  `Descripcion` varchar(200) DEFAULT NULL,
  `Fecha_Inicio` date DEFAULT NULL,
  `Fecha_Fin` date DEFAULT NULL,
  `Estado` varchar(20) DEFAULT NULL,
  `Prioridad` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ID_Actividad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actividades`
--

LOCK TABLES `actividades` WRITE;
/*!40000 ALTER TABLE `actividades` DISABLE KEYS */;
/*!40000 ALTER TABLE `actividades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agentes`
--

DROP TABLE IF EXISTS `agentes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agentes` (
  `id_agente` int(10) NOT NULL,
  `especialidad` varchar(50) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_agente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agentes`
--

LOCK TABLES `agentes` WRITE;
/*!40000 ALTER TABLE `agentes` DISABLE KEYS */;
INSERT INTO `agentes` VALUES (1,'Soporte Técnico','Ana Torres'),(2,'Ventas','Luis Fernández'),(3,'Atención al Cliente','Sofía Martínez');
/*!40000 ALTER TABLE `agentes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bienestar`
--

DROP TABLE IF EXISTS `bienestar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bienestar` (
  `ID_Bienestar` int(8) NOT NULL,
  `Tipo_Beneficio` varchar(50) DEFAULT NULL,
  `Descripcion` varchar(200) DEFAULT NULL,
  `Fecha_Entrega` date DEFAULT NULL,
  `Costo_Beneficio` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID_Bienestar`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bienestar`
--

LOCK TABLES `bienestar` WRITE;
/*!40000 ALTER TABLE `bienestar` DISABLE KEYS */;
/*!40000 ALTER TABLE `bienestar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campañas`
--

DROP TABLE IF EXISTS `campañas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campañas` (
  `id_campaña` int(10) NOT NULL AUTO_INCREMENT,
  `nombre_campaña` varchar(100) DEFAULT NULL,
  `objetivo` varchar(200) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  PRIMARY KEY (`id_campaña`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campañas`
--

LOCK TABLES `campañas` WRITE;
/*!40000 ALTER TABLE `campañas` DISABLE KEYS */;
INSERT INTO `campañas` VALUES (1,'banqueta','bancarme','2025-10-09','2025-10-10');
/*!40000 ALTER TABLE `campañas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente_potencial`
--

DROP TABLE IF EXISTS `cliente_potencial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente_potencial` (
  `id_cliente_potencial` int(10) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `contacto` text DEFAULT NULL,
  PRIMARY KEY (`id_cliente_potencial`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente_potencial`
--

LOCK TABLES `cliente_potencial` WRITE;
/*!40000 ALTER TABLE `cliente_potencial` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente_potencial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int(10) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `contacto` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Juan Pérez','juan.perez@email.com'),(2,'María Gómez','maria.gomez@email.com'),(3,'Carlos Rodríguez','carlos.rodriguez@email.com');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contabilidad`
--

DROP TABLE IF EXISTS `contabilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contabilidad` (
  `ID_Contabilidad` int(8) NOT NULL,
  `Fecha` date DEFAULT NULL,
  `Monto` decimal(12,2) DEFAULT NULL,
  `Descripcion` varchar(200) DEFAULT NULL,
  `Tipo_Transaccion` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID_Contabilidad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contabilidad`
--

LOCK TABLES `contabilidad` WRITE;
/*!40000 ALTER TABLE `contabilidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `contabilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departamentos`
--

DROP TABLE IF EXISTS `departamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departamentos` (
  `ID_departamento` int(8) unsigned NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Presupuesto_Asignado` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`ID_departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamentos`
--

LOCK TABLES `departamentos` WRITE;
/*!40000 ALTER TABLE `departamentos` DISABLE KEYS */;
INSERT INTO `departamentos` VALUES (1,'Direccion',85000.00),(2,'RRHH',120000.00),(3,'Finanzas',65000.00),(4,'Marketing',78000.00),(5,'Servicio al cliente',92000.00),(6,'Logistica',99000.00);
/*!40000 ALTER TABLE `departamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `ID_Empleado` int(8) NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  `Fecha_Contratacion` date DEFAULT NULL,
  `ID_Departamento` int(8) NOT NULL,
  PRIMARY KEY (`ID_Empleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados_rrhh`
--

DROP TABLE IF EXISTS `empleados_rrhh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados_rrhh` (
  `ID_Empleado` int(8) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  `Departamento` varchar(50) DEFAULT NULL,
  `Fecha_Nacimiento` date DEFAULT NULL,
  `Direccion` varchar(100) DEFAULT NULL,
  `Telefono` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Fecha_Contratacion` date DEFAULT NULL,
  `Puesto` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Empleado`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados_rrhh`
--

LOCK TABLES `empleados_rrhh` WRITE;
/*!40000 ALTER TABLE `empleados_rrhh` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleados_rrhh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encuestas`
--

DROP TABLE IF EXISTS `encuestas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `encuestas` (
  `id_encuesta` int(10) NOT NULL,
  `calificacion` int(2) DEFAULT NULL,
  `fecha_realizacion` date DEFAULT NULL,
  `comentarios` varchar(300) DEFAULT NULL,
  `id_ticket` int(10) DEFAULT NULL,
  PRIMARY KEY (`id_encuesta`),
  KEY `id_ticket` (`id_ticket`),
  CONSTRAINT `encuestas_ibfk_1` FOREIGN KEY (`id_ticket`) REFERENCES `tickets` (`id_ticket`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encuestas`
--

LOCK TABLES `encuestas` WRITE;
/*!40000 ALTER TABLE `encuestas` DISABLE KEYS */;
INSERT INTO `encuestas` VALUES (1,5,'2025-10-02','Excelente atención, problema resuelto rápido',1),(2,4,'2025-10-04','Factura enviada correctamente, pero tardó un poco',2),(3,3,'2025-10-06','Asistencia útil, pero aún hay problemas con el sistema',3);
/*!40000 ALTER TABLE `encuestas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horarios`
--

DROP TABLE IF EXISTS `horarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horarios` (
  `ID_Horario` int(8) NOT NULL,
  `ID_Empleado` int(8) NOT NULL,
  `Fecha` date DEFAULT NULL,
  `Hora_Inicio` time DEFAULT NULL,
  `Hora_Fin` time DEFAULT NULL,
  `Tipo_Horario` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ID_Horario`),
  KEY `ID_Empleado` (`ID_Empleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horarios`
--

LOCK TABLES `horarios` WRITE;
/*!40000 ALTER TABLE `horarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `horarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interacciones`
--

DROP TABLE IF EXISTS `interacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interacciones` (
  `id_interaccion` int(10) NOT NULL,
  `fecha_hora` datetime DEFAULT NULL,
  `detalles` varchar(500) DEFAULT NULL,
  `tipo_interaccion` varchar(50) DEFAULT NULL,
  `id_ticket` int(10) DEFAULT NULL,
  PRIMARY KEY (`id_interaccion`),
  KEY `id_ticket` (`id_ticket`),
  CONSTRAINT `interacciones_ibfk_1` FOREIGN KEY (`id_ticket`) REFERENCES `tickets` (`id_ticket`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interacciones`
--

LOCK TABLES `interacciones` WRITE;
/*!40000 ALTER TABLE `interacciones` DISABLE KEYS */;
INSERT INTO `interacciones` VALUES (1,'2025-10-01 10:30:00','Llamada para explicar el problema de internet','Llamada',1),(2,'2025-10-03 14:15:00','Correo enviado con la factura adjunta','Correo',2),(3,'2025-10-05 09:00:00','Chat en línea para asistencia del sistema','Chat',3);
/*!40000 ALTER TABLE `interacciones` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maquinas`
--

LOCK TABLES `maquinas` WRITE;
/*!40000 ALTER TABLE `maquinas` DISABLE KEYS */;
INSERT INTO `maquinas` VALUES (1,'Cinta de correr','Inactivo',2),(2,'Bicicleta fija','Activo',2),(3,'Elíptica','Inactivo',2),(4,'Máquina de pecho','Inactivo',2),(5,'Máquina de piernas','Inactivo',2),(6,'Cinta de correr','Activa',3),(7,'Bicicleta fija','Activa',3),(8,'Elíptica','Activa',3),(9,'Máquina de pecho','Activa',3),(10,'Máquina de piernas','Activa',3),(11,'Cinta de correr','Activa',4),(12,'Bicicleta fija','Activa',4),(13,'Elíptica','Activa',4),(14,'Máquina de pecho','Activa',4),(15,'Máquina de piernas','Activa',4),(16,'Cinta de correr','Activa',5),(17,'Bicicleta fija','Activa',5),(18,'Elíptica','Activa',5),(19,'Máquina de pecho','Activa',5),(20,'Máquina de piernas','Activa',5),(21,'Cinta de correr','Activa',6),(22,'Bicicleta fija','Activa',6),(23,'Elíptica','Activa',6),(24,'Máquina de pecho','Activa',6),(25,'Máquina de piernas','Activa',6),(26,'Cinta de correr','Activa',7),(27,'Bicicleta fija','Activa',7),(28,'Elíptica','Activa',7),(29,'Máquina de pecho','Activa',7),(30,'Máquina de piernas','Activa',7),(31,'Cinta de correr','Activa',8),(32,'Bicicleta fija','Activa',8),(33,'Elíptica','Activa',8),(34,'Máquina de pecho','Activa',8),(35,'Máquina de piernas','Activa',8),(36,'Cinta de correr','Activa',9),(37,'Bicicleta fija','Activa',9),(38,'Elíptica','Activa',9),(39,'Máquina de pecho','Activa',9),(40,'Máquina de piernas','Activa',9),(41,'Cinta de correr','Activa',10),(42,'Bicicleta fija','Activa',10),(43,'Elíptica','Activa',10),(44,'Máquina de pecho','Activa',10),(45,'Máquina de piernas','Activa',10),(46,'Cinta de correr','Activa',11),(47,'Bicicleta fija','Activa',11),(48,'Elíptica','Activa',11),(49,'Máquina de pecho','Activa',11),(50,'Máquina de piernas','Activa',11),(51,'Cinta de correr','Activa',12),(52,'Bicicleta fija','Activa',12),(53,'Elíptica','Activa',12),(54,'Máquina de pecho','Activa',12),(55,'Máquina de piernas','Activa',12),(56,'Cinta de correr','Activa',13),(57,'Bicicleta fija','Activa',13),(58,'Elíptica','Activa',13),(59,'Máquina de pecho','Activa',13),(60,'Máquina de piernas','Activa',13),(61,'Cinta de correr','Activa',14),(62,'Bicicleta fija','Activa',14),(63,'Elíptica','Activa',14),(64,'Máquina de pecho','Activa',14),(65,'Máquina de piernas','Activa',14),(66,'Cinta de correr','Activa',15),(67,'Bicicleta fija','Activa',15),(68,'Elíptica','Activa',15),(69,'Máquina de pecho','Activa',15),(70,'Máquina de piernas','Activa',15),(71,'Cinta de correr','Activa',16),(72,'Bicicleta fija','Activa',16),(73,'Elíptica','Activa',16),(74,'Máquina de pecho','Activa',16),(75,'Máquina de piernas','Activa',16),(76,'Cinta de correr','Activa',17),(77,'Bicicleta fija','Activa',17),(78,'Elíptica','Activa',17),(79,'Máquina de pecho','Activa',17),(80,'Máquina de piernas','Activa',17),(81,'cinta de correr','Activa',18),(82,'cinta de correr','Activa',18),(83,'Jalon al pecho','Activa',18),(84,'Elíptica','Activa',18),(85,'Press banca','Activa',18);
/*!40000 ALTER TABLE `maquinas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `planificacion`
--

DROP TABLE IF EXISTS `planificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planificacion` (
  `ID_Planificacion` int(8) NOT NULL,
  `Fecha` date DEFAULT NULL,
  `Periodo` varchar(20) DEFAULT NULL,
  `Objetivo` varchar(200) DEFAULT NULL,
  `Alcance` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ID_Planificacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planificacion`
--

LOCK TABLES `planificacion` WRITE;
/*!40000 ALTER TABLE `planificacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `planificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presupuestos`
--

DROP TABLE IF EXISTS `presupuestos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presupuestos` (
  `ID_Presupuesto` int(8) NOT NULL,
  `Año` int(4) DEFAULT NULL,
  `Monto_Total` decimal(12,2) DEFAULT NULL,
  `Estado_Presupuesto` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID_Presupuesto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presupuestos`
--

LOCK TABLES `presupuestos` WRITE;
/*!40000 ALTER TABLE `presupuestos` DISABLE KEYS */;
INSERT INTO `presupuestos` VALUES (0,2026,500000000.00,'Aprobado');
/*!40000 ALTER TABLE `presupuestos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int(10) NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reclutamiento`
--

DROP TABLE IF EXISTS `reclutamiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reclutamiento` (
  `ID_Reclutamiento` int(11) NOT NULL AUTO_INCREMENT,
  `Fecha_Solicitud` date DEFAULT NULL,
  `Descripcion_Puesto` varchar(200) DEFAULT NULL,
  `Salario_Ofrecido` decimal(10,2) DEFAULT NULL,
  `Fecha_Cierre` date DEFAULT NULL,
  `Estado_Proceso` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID_Reclutamiento`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reclutamiento`
--

LOCK TABLES `reclutamiento` WRITE;
/*!40000 ALTER TABLE `reclutamiento` DISABLE KEYS */;
INSERT INTO `reclutamiento` VALUES (1,'2025-11-04','Propuesta de Autoregistro - Puesto: Empleado en Área: RRHH. Usuario: tobi inzunza',100.00,'2025-11-04','Aprobado - Contratad'),(2,'2025-11-04','Propuesta de Autoregistro - Puesto: Empleado en Área: RRHH. Usuario: luchi luchi',100.00,'2025-11-04','Aprobado - Contratad'),(3,'2025-11-04','Propuesta de Autoregistro - Puesto: Empleado en Área: RRHH. Usuario: tobi tobi',99999999.99,'2025-11-04','Aprobado - Contratad');
/*!40000 ALTER TABLE `reclutamiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registro_contable`
--

DROP TABLE IF EXISTS `registro_contable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_contable` (
  `ID_Registro_Contable` int(8) NOT NULL,
  `Fecha` date DEFAULT NULL,
  `Monto` decimal(12,2) DEFAULT NULL,
  `Descripcion` varchar(200) DEFAULT NULL,
  `Tipo_Transaccion` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ID_Registro_Contable`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_contable`
--

LOCK TABLES `registro_contable` WRITE;
/*!40000 ALTER TABLE `registro_contable` DISABLE KEYS */;
/*!40000 ALTER TABLE `registro_contable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sedes`
--

DROP TABLE IF EXISTS `sedes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sedes` (
  `idSedes` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(255) NOT NULL,
  `Ubicacion` varchar(255) NOT NULL,
  `cant_Maquinas` varchar(255) NOT NULL,
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
-- Table structure for table `segmentos`
--

DROP TABLE IF EXISTS `segmentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `segmentos` (
  `id_segmento` int(10) NOT NULL AUTO_INCREMENT,
  `nombre_segmento` varchar(100) DEFAULT NULL,
  `criterios_demograficos` text DEFAULT NULL,
  `bordes_segmento` text DEFAULT NULL,
  PRIMARY KEY (`id_segmento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `segmentos`
--

LOCK TABLES `segmentos` WRITE;
/*!40000 ALTER TABLE `segmentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `segmentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicios`
--

DROP TABLE IF EXISTS `servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicios` (
  `id_servicio` int(10) NOT NULL AUTO_INCREMENT,
  `nombre_servicio` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id_servicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicios`
--

LOCK TABLES `servicios` WRITE;
/*!40000 ALTER TABLE `servicios` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sueldos`
--

DROP TABLE IF EXISTS `sueldos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sueldos` (
  `ID_Sueldo` int(8) NOT NULL,
  `Fecha_Pago` date DEFAULT NULL,
  `Monto_Bruto` decimal(12,2) DEFAULT NULL,
  `ID_Empleado` int(8) NOT NULL,
  PRIMARY KEY (`ID_Sueldo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sueldos`
--

LOCK TABLES `sueldos` WRITE;
/*!40000 ALTER TABLE `sueldos` DISABLE KEYS */;
/*!40000 ALTER TABLE `sueldos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `id_ticket` int(10) NOT NULL,
  `fecha_apertura` date DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `asunto` varchar(200) DEFAULT NULL,
  `id_cliente` int(10) DEFAULT NULL,
  PRIMARY KEY (`id_ticket`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (1,'2025-10-01','Problema con la conexión a internet','Abierto','Internet caído',1),(2,'2025-10-03','Consulta sobre factura','Cerrado','Factura octubre',2),(3,'2025-10-05','No funciona el sistema de reservas','En progreso','Error en reservas',3);
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaccion_teso`
--

DROP TABLE IF EXISTS `transaccion_teso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaccion_teso` (
  `ID_Transaccion_Teso` int(8) NOT NULL,
  `Fecha_Transaccion` date DEFAULT NULL,
  `Tipo_Movimiento` varchar(20) DEFAULT NULL,
  `Monto_Movimiento` decimal(12,2) DEFAULT NULL,
  `Descripcion_Movimie` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`ID_Transaccion_Teso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaccion_teso`
--

LOCK TABLES `transaccion_teso` WRITE;
/*!40000 ALTER TABLE `transaccion_teso` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaccion_teso` ENABLE KEYS */;
UNLOCK TABLES;

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
  `Rol` varchar(20) NOT NULL,
  `logueado` tinyint(1) NOT NULL,
  `id_departamento` int(8) unsigned NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `IdUsuario` (`idUsuario`),
  KEY `id_departamento` (`id_departamento`),
  CONSTRAINT `fk_departamento` FOREIGN KEY (`id_departamento`) REFERENCES `departamentos` (`ID_departamento`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
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

-- Dump completed on 2025-11-18 15:54:29
