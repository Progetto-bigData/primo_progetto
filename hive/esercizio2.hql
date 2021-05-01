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
				

CREATE TABLE azione AS
SELECT historical_stock_prices.ticker, YEAR(historical_stock_prices.data) AS year, historical_stocks.sector, (MAX(historical_stock_prices.close) - MIN(historical_stock_prices.close)-1)*100 AS differenza
FROM historical_stock_prices JOIN historical_stocks ON (historical_stock_prices.ticker = historical_stocks.ticker)
GROUP BY historical_stock_prices.ticker, YEAR(historical_stock_prices.data), historical_stocks.sector;

SELECT YEAR(historical_stock_prices.data) AS year, historical_stocks.sector, MAX(azione.differenza) AS diff_percentuale_massima, SUM(historical_stock_prices.close) AS maggiore_incremento, MAX(volume) AS volume_massimo
FROM 
    historical_stocks
    JOIN
    historical_stock_prices
    ON (historical_stocks.ticker = historical_stock_prices.ticker)
    JOIN
    azione
    ON (historical_stocks.ticker = azione.ticker)
GROUP BY YEAR(historical_stock_prices.data), historical_stocks.sector
HAVING YEAR(historical_stock_prices.data) > '2007'
ORDER BY historical_stocks.sector
LIMIT 20;


DROP TABLE historical_stock_prices;
DROP TABLE historical_stocks;
DROP TABLE azione;

