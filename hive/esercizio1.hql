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
				

CREATE TABLE min AS 
SELECT table1.ticker, close
FROM (
    SELECT ticker, MIN(data) AS data_min
    FROM historical_stock_prices
    GROUP BY ticker) AS table1
    JOIN (
    SELECT ticker, data, close
    FROM historical_stock_prices
    GROUP BY ticker, data, close)  AS table2
    ON (table1.ticker = table2.ticker)
WHERE table1.data_min = table2.data;

CREATE TABLE max AS 
SELECT table1.ticker, close
FROM (
    SELECT ticker, MAX(data) AS data_max
    FROM historical_stock_prices
    GROUP BY ticker) AS table1
    JOIN (
    SELECT ticker, data, close
    FROM historical_stock_prices
    GROUP BY ticker, data, close)  AS table2
    ON (table1.ticker = table2.ticker)
WHERE table1.data_max = table2.data;

CREATE TABLE diff AS
SELECT max.ticker, (((max.close / min.close)*100) - 100) AS differenza_percentuale
FROM 
    max 
    JOIN 
    min 
    ON (max.ticker = min.ticker)
GROUP BY max.ticker, max.close, min.close;

SELECT historical_stock_prices.ticker, MIN(historical_stock_prices.data) AS data_prima_quotazione, MAX(historical_stock_prices.data) AS data_ultima_quotazione, diff.differenza_percentuale, MIN(historical_stock_prices.lowThe) AS prezzo_minimo, MAX(historical_stock_prices.highThe) AS prezzo_massimo
FROM 
    historical_stock_prices
    JOIN 
    diff
    ON (historical_stock_prices.ticker = diff.ticker)
GROUP BY historical_stock_prices.ticker, diff.differenza_percentuale
ORDER BY data_ultima_quotazione DESC
LIMIT 20;



DROP TABLE historical_stock_prices;
DROP TABLE min;
DROP TABLE max;
DROP TABLE diff;


