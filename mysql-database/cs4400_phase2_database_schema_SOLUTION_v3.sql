-- CS4400: Introduction to Database Systems (Fall 2024)
-- Project Phase II: Database Schema SOLUTION [v2] Monday, Oct 21, 2024
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

set @thisDatabase = 'business_supply';
drop database if exists business_supply;
create database if not exists business_supply;
use business_supply;

-- -----------------------------------------------
-- table structures
-- -----------------------------------------------

create table users (
username varchar(40) not null,
first_name varchar(100) not null,
last_name varchar(100) not null,
address varchar(500) not null,
birthdate date not null,
primary key (username)
) engine = innodb;

create table employees (
username varchar(40) not null,
taxID varchar(40) not null,
hired date not null,
experience integer not null,
salary integer not null,
primary key (username),
unique key (taxID)
) engine = innodb;

create table business_owners (
username varchar(40) not null,
primary key (username)
) engine = innodb;

create table drivers (
username varchar(40) not null,
licenseID varchar(40) not null,
license_type varchar(100) not null,
successful_trips integer not null,
primary key (username),
unique key (licenseID)
) engine = innodb;

create table workers (
username varchar(40) not null,
primary key (username)
) engine = innodb;

create table products (
barcode varchar(40) not null,
iname varchar(100) not null,
weight integer not null,
primary key (barcode)
) engine = innodb;

create table locations (
label varchar(40) not null,
x_coord integer not null,
y_coord integer not null,
space integer,
primary key (label)
) engine = innodb;

create table businesses (
long_name varchar(40) not null,
rating integer not null,
spent integer not null,
location varchar(40) not null,
primary key (long_name)
) engine = innodb;

create table delivery_services (
id varchar(40) not null,
long_name varchar(100) not null,
home_base varchar(40) not null,
manager varchar(40),
primary key (id),
unique key (manager)
) engine = innodb;

create table vans (
id varchar(40) not null,
tag integer not null,
fuel integer not null,
capacity integer not null,
sales integer not null,
driven_by varchar(40) default null,
located_at varchar(40) not null,
primary key (id, tag)
) engine = innodb;

create table contain (
id varchar(40) not null,
tag integer not null,
barcode varchar(40) not null,
quantity integer not null,
price integer not null,
primary key (id, tag, barcode)
) engine = innodb;

create table work_for (
username varchar(40) not null,
id varchar(40) not null,
primary key (username, id)
) engine = innodb;

create table fund (
username varchar(40) not null, 
invested integer, 
invested_date date not null, 
business varchar(40) not null, 
primary key (username, business)
) engine=innodb;

-- -----------------------------------------------
-- referential structures
-- -----------------------------------------------

alter table employees add constraint fk1 foreign key (username) references users (username)
	on update cascade on delete cascade;
alter table business_owners add constraint fk2 foreign key (username)
	references users (username) on update cascade on delete cascade;
alter table drivers add constraint fk3 foreign key (username) references employees (username)
	on update cascade on delete cascade;
alter table workers add constraint fk4 foreign key (username) references employees (username)
	on update cascade on delete cascade;
alter table businesses add constraint fk10 foreign key (location) references locations (label)
	on update cascade;
alter table delivery_services add constraint fk11 foreign key (home_base)
	references locations (label) on update cascade;
alter table delivery_services add constraint fk15 foreign key (manager)
	references workers (username);
alter table vans add constraint fk5 foreign key (id) references delivery_services (id);
alter table vans add constraint fk13 foreign key (driven_by) references drivers (username);
alter table vans add constraint fk16 foreign key (located_at) references locations (label)
	on update cascade;
alter table contain add constraint fk6 foreign key (id, tag) references vans (id, tag);
alter table contain add constraint fk7 foreign key (barcode) references products (barcode);
alter table work_for add constraint fk8 foreign key (username) references employees (username);
alter table work_for add constraint fk9 foreign key (id) references delivery_services (id);
alter table fund add constraint fk17 foreign key (username) references business_owners (username);
alter table fund add constraint fk18 foreign key (business) references businesses (long_name);

-- -----------------------------------------------
-- table data
-- -----------------------------------------------

insert into users (username, first_name, last_name, address, birthdate) values
('agarcia7', 'Alejandro', 'Garcia', '710 Living Water Drive', '1966-10-29'),
('awilson5', 'Aaron', 'Wilson', '220 Peachtree Street', '1963-11-11'),
('bsummers4', 'Brie', 'Summers', '5105 Dragon Star Circle', '1976-02-09'),
('cjordan5', 'Clark', 'Jordan', '77 Infinite Stars Road', '1966-06-05'),
('ckann5', 'Carrot', 'Kann', '64 Knights Square Trail', '1972-09-01'),
('csoares8', 'Claire', 'Soares', '706 Living Stone Way', '1965-09-03'),
('echarles19', 'Ella', 'Charles', '22 Peachtree Street', '1974-05-06'),
('eross10', 'Erica', 'Ross', '22 Peachtree Street', '1975-04-02'),
('fprefontaine6', 'Ford', 'Prefontaine', '10 Hitch Hikers Lane', '1961-01-28'),
('hstark16', 'Harmon', 'Stark', '53 Tanker Top Lane', '1971-10-27'),
('jstone5', 'Jared', 'Stone', '101 Five Finger Way', '1961-01-06'),
('lrodriguez5', 'Lina', 'Rodriguez', '360 Corkscrew Circle', '1975-04-02'),
('mrobot1', 'Mister', 'Robot', '10 Autonomy Trace', '1988-11-02'),
('mrobot2', 'Mister', 'Robot', '10 Clone Me Circle', '1988-11-02'),
('rlopez6', 'Radish', 'Lopez', '8 Queens Route', '1999-09-03'),
('sprince6', 'Sarah', 'Prince', '22 Peachtree Street', '1968-06-15'),
('tmccall5', 'Trey', 'McCall', '360 Corkscrew Circle', '1973-03-19'),
('jdoe1', 'John', 'Doe', '123 Maple Avenue', '1980-02-19'), 
('asmith2', 'Alice', 'Smith', '456 Oak Street', '1975-07-11'),
('bwilliams3', 'Brian', 'Williams', '789 Pine Lane', '1990-11-30'),
('cmartin4', 'Carla', 'Martin', '321 Cedar Drive', '1985-04-05'),
('rjones5', 'Rachel', 'Jones', '654 Birch Boulevard', '1978-12-22'),
('twhite7', 'Tom', 'White', '987 Willow Way', '1965-10-17'),
('mking8', 'Michael', 'King', '432 Elm Road', '1992-08-09'),
('djohnson9', 'Diane', 'Johnson', '876 Aspen Circle', '1983-01-27'),
('krobinson10', 'Karen', 'Robinson', '159 Redwood Avenue', '1971-09-03'),
('cwilson11', 'Charles', 'Wilson', '246 Hickory Lane', '1988-03-14');

insert into employees (username, taxID, hired, experience, salary) values
('agarcia7', '999-99-9999', '2019-03-17', 24, 41000),
('awilson5', '111-11-1111', '2020-03-15', 9, 46000),
('bsummers4', '000-00-0000', '2018-12-06', 17, 35000),
('ckann5', '640-81-2357', '2019-08-03', 27, 46000),
('csoares8', '888-88-8888', '2019-02-25', 26, 57000),
('echarles19', '777-77-7777', '2021-01-02', 3, 27000),
('eross10', '444-44-4444', '2020-04-17', 10, 61000),
('fprefontaine6', '121-21-2121', '2020-04-19', 5, 20000),
('hstark16', '555-55-5555', '2018-07-23', 20, 59000),
('lrodriguez5', '222-22-2222', '2019-04-15', 20, 58000),
('mrobot1', '101-01-0101', '2015-05-27', 8, 38000),
('mrobot2', '010-10-1010', '2015-05-27', 8, 38000),
('rlopez6', '123-58-1321', '2017-02-05', 51, 64000),
('tmccall5', '333-33-3333', '2018-10-17', 29, 33000),
('jdoe1', '123-45-6789', '2020-08-21', 30, 55000),
('asmith2', '234-56-7890', '2018-05-11', 28, 62000),
('bwilliams3', '345-67-8901', '2019-12-15', 33, 48000),
('cmartin4', '456-78-9012', '2021-04-10', 25, 54000),
('rjones5', '567-89-0123', '2022-09-30', 29, 59000);

insert into business_owners (username) values
('cjordan5'), ('jstone5'), ('sprince6'), 
('twhite7'),('mking8'),('djohnson9'),('krobinson10'),('cwilson11');

insert into drivers (username, licenseID, license_type, successful_trips) values
('agarcia7', '610623', 'CDL', 38), 
('awilson5', '314159', 'commercial', 41), 
('bsummers4', '411911', 'private', 35), 
('csoares8', '343563', 'commerical', 7), 
('fprefontaine6', '657483', 'private', 2), 
('lrodriguez5', '287182', 'CDL', 67), 
('mrobot1', '101010', 'CDL', 18), 
('rlopez6', '235711', 'private', 58),
('jdoe1', '326167', 'commercial', 6);

insert into workers (username) values
('ckann5'), 
('echarles19'), 
('eross10'),
('hstark16'), 
('mrobot2'), 
('tmccall5'),
('asmith2'),
('bwilliams3');

insert into products (barcode, iname, weight) values
('gc_4C6B9R', 'glass cleaner', 4), 
('pn_2D7Z6C', 'pens', 5), 
('sd_6J5S8H', 'screwdrivers', 4), 
('pt_16WEF6', 'paper towels', 6), 
('st_2D4E6L', 'shipping tape', 3), 
('hm_5E7L23M', 'hammer', 3),
('gl_5R3Y9K', 'glue sticks', 12),
('hd_7T6Q1B', 'hand sanitizer', 8),
('tp_9J2D4L', 'toilet paper', 24),
('mk_1F7S9V', 'markers', 15),
('pn_3G8D5Q', 'pens', 20),
('nt_4X3K7P', 'notebooks', 10),
('rb_8N2V1W', 'rubber bands', 50),
('pb_6W3J8L', 'push buttons', 40),
('cf_2H4R9T', 'coffee filters', 100),
('ct_5B1N6V', 'cotton balls', 75);

insert into locations (label, x_coord, y_coord, space) values 
('airport', 5, -6, 15), 
('downtown', -4, -3, 10), 
('springs', 7, 10, 8), 
('buckhead', 7, 10, 8), 
('avalon', 2, 15, 12), 
('mercedes', -8, 5, NULL), 
('highlands', 2, 1, 7), 
('southside', 1, -16, 5), 
('midtown', 2, 1, 7),
('plaza', -4, -3, 10), 
('highpoint', 11, 3, 4),
('garnett', 6, 2, 6),
('reynoldstown', 3, -4, 6),
('inman',1, 12, 5),
('uptown', 2, 8, 3),
('riverdale', 2, 9, 4),
('greenwood', 1, 20, 8),
('oakwood', 4, 11, 5),
('springfield', 2, 14, 6),
('lincolnpark', 1, 18, 9),
('brookside', 3, 7, 4),
('willowcreek', 2, 13, 0);

insert into businesses (long_name, rating, spent, location) values
('Aircraft Electrical Svc', 5, 10, 'airport'),
('Homestead Insurance', 5, 30, 'downtown'),
('Jones and Associates', 3, 0, 'springs'),
('Prime Solutions', 4, 30, 'buckhead'),
('Innovative Ventures', 4, 0, 'avalon'),
('Blue Horizon Enterprises', 4, 10, 'mercedes'),
('Peak Performance Group', 5, 20, 'highlands'),
('Summit Strategies', 2, 0, 'southside'),
('Elevate Consulting', 5, 30, 'midtown'),
('Pinnacle Partners', 4, 10, 'plaza');

insert into delivery_services (id, long_name, home_base, manager) values
('mbm', 'Metro Business Movers', 'garnett', 'hstark16'),
('lcc', 'Local Commerce Couriers', 'reynoldstown', 'eross10'),
('pbl', 'Pro Business Logistics', 'inman', 'echarles19');

insert into vans (id, tag, fuel, capacity, sales, driven_by, located_at) values
('mbm', '1', 100, 6, 0, 'fprefontaine6', 'southside'),
('mbm', '5', 27, 7, 100, 'fprefontaine6', 'buckhead'),
('mbm', '8', 100, 8, 0, 'bsummers4', 'southside'),
('mbm','11',  25, 10, 0, NULL, 'buckhead'),
('mbm','16', 17, 5, 40, 'fprefontaine6', 'buckhead'),
('mbm','20', 17, 5, 40, NULL, 'garnett'),
('lcc', '1', 100, 9, 0, 'awilson5', 'airport'),
('lcc', '2', 75, 7, 0, NULL, 'airport'),
('pbl','3',  100, 5, 50, 'agarcia7', 'avalon'),
('pbl','7', 53, 5, 100, 'agarcia7', 'avalon'),
('pbl','8',  100, 6, 0, 'agarcia7', 'inman'),
('pbl', '11', 90, 6, 0, NULL, 'inman');

insert into contain (tag, ID, barcode, price, quantity) values
('3', 'pbl', 'pn_2D7Z6C', 28, 2),
('5', 'mbm', 'pn_2D7Z6C', 30, 1),
('1', 'lcc', 'pt_16WEF6', 20, 5),
('8', 'mbm', 'pt_16WEF6', 18, 4),
('1', 'lcc', 'st_2D4E6L', 23, 3),
('11', 'mbm', 'st_2D4E6L', 19, 3),
('1', 'mbm', 'st_2D4E6L', 27, 6),
('2', 'lcc', 'hm_5E7L23M', 14, 7),
('3', 'pbl', 'hm_5E7L23M', 15, 2),
('5', 'mbm', 'hm_5E7L23M', 17, 4);

insert into work_for (username, ID) values
('ckann5', 'lcc'),
('echarles19', 'pbl'),
('eross10', 'lcc'),
('hstark16', 'mbm'),
('tmccall5', 'mbm'), 
('tmccall5', 'lcc'), 
('mrobot2', 'pbl');

insert into fund (username, invested, invested_date, business) values
('jstone5', 20, '2022-10-25', 'Jones and Associates'),
('sprince6', 10, '2022-03-06', 'Blue Horizon Enterprises'),
('jstone5', 30, '2022-09-08', 'Peak Performance Group'),
('jstone5', 5, '2022-07-25', 'Elevate Consulting');

