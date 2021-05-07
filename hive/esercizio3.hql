CREATE TABLE historical_stock_prices (ticker STRING,
                   open FLOAT,
                   close FLOAT,
                   adj_close FLOAT,
                   lowThe FLOAT,
                   highThe FLOAT,
                   volume INT,
                   data DATE)
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ",";

LOAD DATA LOCAL INPATH "Documents/big_data/hive_prova/historical_stock_prices.csv"
				OVERWRITE INTO TABLE historical_stock_prices;

CREATE TABLE historical_stocks (ticker STRING,
                   exchang STRING,
                   name STRING,
                   sector STRING,
                   industry STRING)
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ",";

LOAD DATA LOCAL INPATH "Documents/big_data/hive_prova/historical_stocks_cleaned.csv"
				OVERWRITE INTO TABLE historical_stocks;



CREATE TABLE anno2017 AS
SELECT historical_stock_prices.ticker, MAX(historical_stock_prices.data) AS data_max, MIN(historical_stock_prices.data) AS data_min, historical_stocks.name AS name
FROM    
    historical_stock_prices
    JOIN
    historical_stocks
    ON (historical_stock_prices.ticker == historical_stocks.ticker)
WHERE YEAR(historical_stock_prices.data) = '2017'
GROUP BY historical_stock_prices.ticker, historical_stocks.name, MONTH(historical_stock_prices.data);

CREATE TABLE close_max AS
SELECT historical_stock_prices.ticker, historical_stock_prices.close AS close_max, anno2017.data_max AS data_max, anno2017.name AS name
FROM 
    anno2017
    JOIN
    historical_stock_prices
    ON (anno2017.ticker = historical_stock_prices.ticker)
WHERE anno2017.data_max = historical_stock_prices.data AND YEAR(historical_stock_prices.data) = '2017';

CREATE TABLE close_min AS
SELECT historical_stock_prices.ticker, historical_stock_prices.close AS close_min, anno2017.data_min AS data_min, anno2017.name AS name
FROM 
    anno2017
    JOIN
    historical_stock_prices
    ON (anno2017.ticker = historical_stock_prices.ticker)
WHERE anno2017.data_min = historical_stock_prices.data AND YEAR(historical_stock_prices.data) = '2017';

CREATE TABLE varianza AS
SELECT close_max.ticker, (((close_max.close_max / close_min.close_min)-1)*100) AS var_mensile, MONTH(close_max.data_max) AS month, close_max.name AS name
FROM 
    close_max
    JOIN
    close_min
    ON (close_max.ticker = close_min.ticker)
WHERE MONTH(close_max.data_max) = MONTH(close_min.data_min);


CREATE TABLE varianza_coppia AS
SELECT v1.month AS month, v1.ticker AS first_ticker, v1.var_mensile AS first_var_mensile, v2.ticker AS second_ticker, v2.var_mensile AS second_var_mensile, v1.name AS first_name, v2.name AS second_name
FROM 
    varianza v1
    JOIN
    varianza v2
    ON (v1.month = v2.month)
WHERE ABS(v1.var_mensile - v2.var_mensile) <= 1 AND v1.ticker > v2.ticker;

CREATE TABLE coppie_buone AS
SELECT varianza_coppia.first_ticker AS first_ticker, varianza_coppia.second_ticker AS second_ticker, COUNT(*) as conto
FROM varianza_coppia
GROUP BY varianza_coppia.first_ticker, varianza_coppia.second_ticker
HAVING conto = 12;


SELECT varianza_coppia.month, varianza_coppia.first_name, varianza_coppia.first_var_mensile, varianza_coppia.second_name, varianza_coppia.second_var_mensile
FROM 
    varianza_coppia
    JOIN
    coppie_buone
    ON (varianza_coppia.first_ticker = coppie_buone.first_ticker AND varianza_coppia.second_ticker = coppie_buone.second_ticker)
ORDER BY varianza_coppia.first_name, varianza_coppia.second_name, varianza_coppia.month
LIMIT 48;


DROP TABLE historical_stock_prices;
DROP TABLE historical_stocks;
DROP TABLE anno2017;
DROP TABLE close_min;
DROP TABLE close_max;
DROP TABLE varianza;
DROP TABLE varianza_coppia;
DROP TABLE coppie_buone;
 
