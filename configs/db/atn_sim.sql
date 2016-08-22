-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema atn_sim
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `atn_sim` ;

-- -----------------------------------------------------
-- Schema atn_sim
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `atn_sim` DEFAULT CHARACTER SET utf8 ;
USE `atn_sim` ;

-- -----------------------------------------------------
-- Table `atn_sim`.`node`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `atn_sim`.`node` ;

CREATE TABLE IF NOT EXISTS `atn_sim`.`node` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `session` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `atn_sim`.`nem`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `atn_sim`.`nem` ;

CREATE TABLE IF NOT EXISTS `atn_sim`.`nem` (
  `nem` INT NOT NULL,
  `node_id` INT NULL,
  `iface` VARCHAR(45) NULL,
  `ip` VARCHAR(45) NULL,
  `latitude` DOUBLE NULL DEFAULT 0,
  `longitude` DOUBLE NULL DEFAULT 0,
  `altitude` DOUBLE NULL DEFAULT 0,
  `pitch` DOUBLE NULL DEFAULT 0,
  `roll` DOUBLE NULL DEFAULT 0,
  `yaw` DOUBLE NULL DEFAULT 0,
  `azimuth` DOUBLE NULL DEFAULT 0,
  `elevation` DOUBLE NULL DEFAULT 0,
  `magnitude` DOUBLE NULL DEFAULT 0,
  `last_update` TIMESTAMP NULL DEFAULT now(),
  PRIMARY KEY (`nem`),
  INDEX `fk_nem_node_idx` (`node_id` ASC))
ENGINE = MEMORY
COMMENT = '\n';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
