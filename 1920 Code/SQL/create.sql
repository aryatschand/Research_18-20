CREATE TABLE irrigation_data (id int not null auto_increment, plant_num int, water double, color int, temperature int, photoresistance int, image varchar(255), primary key(id));

CREATE TABLE drone (id int not null auto_increment, demo int, nextLocation varchar(255), primary key(id));

CREATE TABLE micropiece_commands (id int not null auto_increment, plant_num int, water_volume double, empirical double, theoretical double, notes varchar(255), primary key(id));

CREATE TABLE rfid_location (id int not null auto_increment, rfid_num varchar(255), plant_num int, x_location int, y_location int, primary key(id));