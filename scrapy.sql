/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50640
Source Host           : localhost:3306
Source Database       : scrapy

Target Server Type    : MYSQL
Target Server Version : 50640
File Encoding         : 65001

Date: 2018-05-28 22:46:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for music_163_com_comments
-- ----------------------------
DROP TABLE IF EXISTS `music_163_com_comments`;
CREATE TABLE `music_163_com_comments` (
  `songId` varchar(32) CHARACTER SET utf8mb4 NOT NULL,
  `songName` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `nickname` varchar(120) CHARACTER SET utf8mb4 NOT NULL,
  `beRepliedContent` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `time` datetime NOT NULL,
  `content` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`songId`,`nickname`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Procedure structure for add_uniq_music_163_com_comments
-- ----------------------------
DROP PROCEDURE IF EXISTS `add_uniq_music_163_com_comments`;
DELIMITER ;;
CREATE  PROCEDURE `add_uniq_music_163_com_comments`(IN `isongId` longtext,IN `isongName` longtext,IN `inickname` longtext,IN `ibeRepliedContent` longtext,IN `itime` datetime,IN `icontent` longtext)
BEGIN
	
  SELECT count(*) INTO @tmpNum  FROM music_163_com_comments WHERE songId=isongId and nickname=inickname and time=itime;

	IF @tmpNum=0 THEN
	
	  INSERT INTO `music_163_com_comments` (`songId`, `songName`, `nickname`, `beRepliedContent`, `time`, `content`) VALUES (isongId, isongName, inickname, ibeRepliedContent,itime, icontent);
  END IF;

END
;;
DELIMITER ;
