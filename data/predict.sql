DROP TABLE IF EXISTS sales_analytics.scoring_ml_antoniovf;

CREATE TABLE sales_analytics.scoring_ml_antoniovf (
    store_id INT,
    date_sale DATE,
    year INT,
    month INT,
    day INT,
    weekday INT,
    total_sales NUMERIC(10,2)
);

INSERT INTO sales_analytics.scoring_ml_antoniovf(
    store_id,
    date_sale
) SELECT
    store.store_id,
    generate_series(
        CURRENT_DATE,
        CURRENT_DATE + INTERVAL '6 days',
        INTERVAL '1 day'
    )::DATE AS date_sale
FROM
    (
        SELECT store_id
        FROM sales.item_sale
        GROUP BY store_id
    ) AS store;

UPDATE 
    sales_analytics.scoring_ml_antoniovf
SET
    year = EXTRACT(YEAR FROM date_sale),
    month = EXTRACT(MONTH FROM date_sale),
    day = EXTRACT(DAY FROM date_sale),
    weekday = EXTRACT(DOW FROM date_sale),
    total_sales = NULL;

ALTER TABLE 
    sales_analytics.scoring_ml_antoniovf 
DROP COLUMN 
    date_sale;

SELECT 
    store_id, 
    year, 
    month, 
    day,
    weekday, 
    total_sales
FROM 
    sales_analytics.scoring_ml_antoniovf
ORDER BY
    store_id,
    year,
    month,
    day,
    weekday;