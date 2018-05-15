-- create by Ben.
-- 如果存在先删除库
drop database if exists ilweibo;
-- 建库
create database ilweibo;

use ilweibo;

grant select, insert, update, delete on ilweibo.* to 'www-data'@'localhost' identified by 'www-data';

-- 建表
create table comments (
    `pic` text(300),
    `text` text(300),
    `name` text(30),
	`id` VARCHAR(512) not null,
   	primary key (`id`)
) engine=innodb default charset=utf8;

