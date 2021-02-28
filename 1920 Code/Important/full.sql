CREATE TABLE irrigation_data (id int not null auto_increment, plant_num int, water double, color int, temperature int, photoresistance int, image varchar(255), primary key(id));

CREATE TABLE drone (id int not null auto_increment, demo int, nextLocation varchar(255), primary key(id));

CREATE TABLE micropiece_commands (id int not null auto_increment, plant_num int, water_volume double, empirical double, theoretical double, notes varchar(255), primary key(id));

CREATE TABLE rfid_location (id int not null auto_increment, rfid_num varchar(255), plant_num int, x_location int, y_location int, primary key(id));

DECLARE @plantNum int
DECLARE @water int
DECLARE @color int
DECLARE @temperature int
DECLARE @photoresistance int
DECLARE @image varchar(255)
INSERT INTO `irrigation_data` (`id`, `plant_num`, `water`,`color`,`temperature`, `photoresistance`, `image`) VALUES (NULL, @plantNum, @water, @color, @temperature, @photoresistance, @image);

DECLARE @demo int
DECLARE @nextLocation varchar(255)
INSERT INTO `drone`(`id`, `demo`, `nextLocation`) VALUES (NULL, @demo, @nextLocation);

DECLARE @plantNum int
DECLARE @water int
DECLARE @empirical int
DECLARE @theoretical int
DECLARE @notes varchar(255)
INSERT INTO `micropiece_commands` (`id`, `plant_num`, `water_volume`,`empirical`,`theoretical`, `notes`) VALUES (NULL, @plantNum, @water, @empirical, @theoretical, @notes);

DECLARE @RFID varchar(255)
DECLARE @plantNum int
DECLARE @xLocation int
DECLARE @yLocation int
INSERT INTO `rfid_location` (`id`, `rfid_num`, `plant_num`, `x_location`, `y_location`) VALUES (NULL, @RFID, @plantNum, @xLocation, @yLocation);