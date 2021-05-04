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
				

CREATE TABLE intermediate AS
SELECT historical_stock_prices.ticker, historical_stocks.sector, YEAR(historical_stock_prices.data) AS year, MIN(historical_stock_prices.data) AS data_min, MAX(historical_stock_prices.data) AS data_max, SUM(historical_stock_prices.volume) AS volume
FROM historical_stock_prices JOIN historical_stocks ON (historical_stock_prices.ticker = historical_stocks.ticker)
GROUP BY historical_stock_prices.ticker, YEAR(historical_stock_prices.data), historical_stocks.sector
HAVING YEAR(historical_stock_prices.data) > '2008' AND YEAR(historical_stock_prices.data) < '2019';

CREATE TABLE close_min AS
SELECT historical_stock_prices.ticker, YEAR(historical_stock_prices.data) AS year, intermediate.sector, historical_stock_prices.close AS close, intermediate.volume AS volume
FROM historical_stock_prices JOIN intermediate ON (historical_stock_prices.ticker = intermediate.ticker)
WHERE historical_stock_prices.data = intermediate.data_min
GROUP BY historical_stock_prices.ticker, YEAR(historical_stock_prices.data), intermediate.sector, historical_stock_prices.close, intermediate.volume
HAVING YEAR(historical_stock_prices.data) > '2008' AND YEAR(historical_stock_prices.data) < '2019';

CREATE TABLE close_max AS
SELECT historical_stock_prices.ticker, YEAR(historical_stock_prices.data) AS year, intermediate.sector, historical_stock_prices.close AS close
FROM historical_stock_prices JOIN intermediate ON (historical_stock_prices.ticker = intermediate.ticker)
WHERE historical_stock_prices.data = intermediate.data_max
GROUP BY historical_stock_prices.ticker, YEAR(historical_stock_prices.data), intermediate.sector, historical_stock_prices.close
HAVING YEAR(historical_stock_prices.data) > '2008' AND YEAR(historical_stock_prices.data) < '2019';

SELECT close_min.year, close_min.sector, ((SUM(close_max.close) / SUM(close_min.close)-1)*100) AS diff_percentuale, MAX(close_max.close - close_min.close) AS maggiore_incremento, MAX(close_min.volume) AS volume_massimo
FROM 
    close_min
    JOIN
    close_max
    ON (close_min.ticker = close_max.ticker)
WHERE (close_min.year = close_max.year AND close_min.sector = close_max.sector)
GROUP BY close_min.year, close_min.sector
HAVING close_min.year > '2008' AND close_min.year < '2019'
ORDER BY close_min.sector
LIMIT 20;


DROP TABLE historical_stock_prices;
DROP TABLE historical_stocks;
DROP TABLE close_min;
DROP TABLE close_max;
DROP TABLE intermediate;

