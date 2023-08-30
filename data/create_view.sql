CREATE VIEW sales_analytics.view_abt_train_antoniovf AS
    SELECT
        store_id,
        EXTRACT(YEAR FROM date_sale) AS year,
        EXTRACT(MONTH FROM date_sale) AS month,
        EXTRACT(DAY FROM date_sale) AS day,
        EXTRACT(DOW FROM date_sale) AS weekday,
        SUM(price) AS total_sales
    FROM sales.item_sale
    WHERE date_sale < CURRENT_DATE - INTERVAL '1 day' AND date_sale > CURRENT_DATE - INTERVAL '1 year' 
    GROUP BY
        store_id,
        date_sale,
        weekday;