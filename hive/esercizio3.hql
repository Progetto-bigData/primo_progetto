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
SELECT historical_stock_prices.ticker,historical_stock_prices.data,historical_stock_prices.close, historical_stocks.name
FROM
    historical_stock_prices
    JOIN
    historical_stocks
    ON (historical_stock_prices.ticker = historical_stocks.ticker)
WHERE YEAR(historical_stock_prices.data) = '2017';

SELECT table1.name AS primo_nome, table2.name AS secondo_nome, table1.close AS primo_close, table2.close AS secondo_close, table1.data, table2.data
FROM 
    anno2017 AS table1
    JOIN 
    anno2017 AS table2
    ON (MONTH(table1.data) = MONTH(table2.data))
LIMIT 500;


DROP TABLE historical_stock_prices;
DROP TABLE historical_stocks;
DROP TABLE anno2017;

