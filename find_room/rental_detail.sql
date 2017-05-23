create database find_room;

create table rental_detail (
id int not null auto_increment,
url varchar(256) not null,
rent int not null,
deposit varchar(40),
rental_method varchar(40),
housing_size varchar(60) not null,
face_floor varchar(60) not null,
locate_detail varchar(60) not null,
locate varchar(40),
release_at timestamp,
created_at timestamp null default current_timestamp,
primary key (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table place_location (
id int not null auto_increment,
rental_id int not null,
lat varchar(15) not null,
lng varchar(15) not null,
primary key (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;