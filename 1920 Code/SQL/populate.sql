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