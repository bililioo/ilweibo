/*
 Navicat Premium Data Transfer

 Source Server         : RootSQL
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : ilweibo

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 15/05/2018 15:11:41
*/

drop database if exists ilweibo;
-- 建库
'www-data';create database ilweibo;

use ilweibo;

grant select, insert, update, delete on ilweibo.* to 'www-data'@'localhost' identified by 

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `pic` text,
  `text` text,
  `name` tinytext,
  `r_uid` text,
  `id` varchar(512) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for weibo
-- ----------------------------
DROP TABLE IF EXISTS `weibo`;
CREATE TABLE `weibo` (
  `pic` text,
  `text` text,
  `name` tinytext,
  `r_uid` text,
  `id` varchar(512) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
