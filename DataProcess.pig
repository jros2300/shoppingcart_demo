A = LOAD 's3://shoppingcart-summit/*' USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:int,product:int');


DATA = LOAD 's3://shoppingcart-summit/streams/*/*/*/*/*' USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:long,product:chararray');

DATA = LOAD 's3://shoppingcart-summit/streams/$inputdate/*' USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:long,product:chararray');

DATA = LOAD 's3://shoppingcart-summit/streams/*/*/*/*/*' USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:long,product:chararray, productlist: chararray');


DATA = LOAD 's3://shoppingcart-summit/streams/$inputdate/*/*' USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:long,product:chararray, productlist: chararray');
DATA2 = FILTER DATA BY type is not null;
CARTS = GROUP DATA2 BY cart;
CARTDATA = FOREACH CARTS { 
	LOGIN = FILTER DATA2 BY type == 'login';
	ADDED = FILTER DATA2 BY type == 'productAdded';
	REMOVED = FILTER DATA2 BY type == 'productRemoved';
	BUY = FILTER DATA2 BY type == 'cartBuy';
	BUYORDISCART = FILTER DATA2 BY type == 'cartBuy' OR type == 'cartDiscard';
	GENERATE MAX(DATA2.customer) AS customer, group AS cart, MAX(DATA2.timestamp)-MIN(LOGIN.timestamp) AS duration, 
		IsEmpty(BUY) AS buy, COUNT_STAR(ADDED) AS added, 
		COUNT_STAR(REMOVED) AS removed, MAX(DATA2.timestamp)-MAX(ADDED.timestamp) AS thinking,
		BagToString(ADDED.product, '-') AS productsadded, BagToString(REMOVED.product, '-') AS productsremoved,
		BagToString(BUYORDISCART.productlist, '-'), MIN(LOGIN.timestamp) AS timestamp;
};
STORE CARTDATA INTO 's3://shoppingcart-summit/ml/$inputdate/' USING PigStorage(',');

DATA = LOAD 's3://shoppingcart-summit/streams/$inputdate/*' USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:long,product:chararray, productlist: chararray');
DATA2 = FILTER DATA BY type is not null;
CARTS = GROUP DATA2 BY cart;
CARTDATA = FOREACH CARTS { 
	LOGIN = FILTER DATA2 BY type == 'login';
	ADDED = FILTER DATA2 BY type == 'productAdded';
	REMOVED = FILTER DATA2 BY type == 'productRemoved';
	BUY = FILTER DATA2 BY type == 'cartBuy';
	GENERATE MAX(DATA2.customer) AS customer, group AS cart, MAX(DATA2.timestamp)-MIN(DATA2.timestamp) AS duration, 
		IsEmpty(BUY) AS buy, COUNT_STAR(ADDED) AS added, 
		COUNT_STAR(REMOVED) AS removed, MAX(DATA2.timestamp)-MAX(ADDED.timestamp) AS thinking,
		MIN(LOGIN.timestamp) AS timestamp, '""';
};
STORE CARTDATA INTO 's3://shoppingcart-summit/redshift/$inputdate/' USING PigStorage(',');

FFF = FILTER DATA2 BY cart == 459241853005102974L;
DUMP FFF;

inputdate=#{format(@scheduledStartTime,'YYYY/MM/dd/HH')}

CREATE TABLE shoppingcart (
	customer INTEGER,
	cart BIGINT,
	duration INTEGER,
	buy VARCHAR(10),
	added INTEGER,
	removed INTEGER,
	thinking INTEGER,
	cartstart BIGINT
) distkey (cart)




DATA = LOAD CONCAT(CONCAT('s3://shoppingcart-summit/streams/'), '*/*/*/*'), '/*') USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:long,product:chararray');

B = JOIN ADDED BY product LEFT OUTER, REMOVED BY product;
C = FILTER B BY REMOVED::product is null;


B = GROUP DATA2 BY type;
X = FOREACH B GENERATE group,COUNT_STAR(DATA2);

DUMP X

DESCRIBE X


A = LOAD 's3://shoppingcart-summit/streams/*/*/*/*/*';
B = limit A 10;
USING JsonLoader('type:chararray,timestamp:int,customer:int,cart:long,product:int');


A = FOREACH CARTS GENERATE group AS cart,COUNT_STAR(DATA2), MAX(DATA2.timestamp), MIN(DATA2.timestamp);