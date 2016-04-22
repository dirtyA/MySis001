/*
Navicat MySQL Data Transfer

Source Server         : ws.com
Source Server Version : 50627
Source Host           : ws.com:3347
Source Database       : SisDB

Target Server Type    : MYSQL
Target Server Version : 50627
File Encoding         : 65001

Date: 2016-04-22 22:26:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for c_original
-- ----------------------------
DROP TABLE IF EXISTS `c_original`;
CREATE TABLE `c_original` (
  `tid` char(30) NOT NULL,
  `tag` char(30) NOT NULL,
  `title` char(255) NOT NULL,
  `url` char(60) NOT NULL,
  `posttime` date NOT NULL,
  `capacity` int(11) DEFAULT NULL,
  `videotype` char(10) DEFAULT NULL,
  `view` int(11) DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for c_reprint
-- ----------------------------
DROP TABLE IF EXISTS `c_reprint`;
CREATE TABLE `c_reprint` (
  `tid` char(30) NOT NULL,
  `tag` char(30) NOT NULL,
  `title` char(255) NOT NULL,
  `url` char(60) NOT NULL,
  `posttime` date NOT NULL,
  `capacity` int(11) DEFAULT NULL,
  `videotype` char(10) DEFAULT NULL,
  `view` int(11) DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for original
-- ----------------------------
DROP TABLE IF EXISTS `original`;
CREATE TABLE `original` (
  `tid` char(30) NOT NULL,
  `tag` char(30) NOT NULL,
  `title` char(255) NOT NULL,
  `url` char(60) NOT NULL,
  `posttime` date NOT NULL,
  `capacity` int(11) DEFAULT NULL,
  `videotype` char(10) DEFAULT NULL,
  `view` int(11) DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for reprint
-- ----------------------------
DROP TABLE IF EXISTS `reprint`;
CREATE TABLE `reprint` (
  `tid` char(30) NOT NULL,
  `tag` char(30) NOT NULL,
  `title` char(255) NOT NULL,
  `url` char(60) NOT NULL,
  `posttime` date NOT NULL,
  `capacity` int(11) DEFAULT NULL,
  `videotype` char(10) DEFAULT NULL,
  `view` int(11) DEFAULT NULL,
  `comment` int(11) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
