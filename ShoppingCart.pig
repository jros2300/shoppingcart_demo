/* Data processing for Redshift */


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



/* Data processing for Machine Learning */


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


