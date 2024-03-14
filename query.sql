SELECT 
    doc_id AS news_id,
    title,
    regexp_replace(
        regexp_replace(content, '<[^>]+>', ''), 
        '</[^>]+>', 
        ''
    ) AS content_clean,
    cat_lv1,
    cat_lv2,
    tags,
    url,
    event_date
FROM etl_ettoday_news
WHERE event_date BETWEEN '2023-07-01' AND '2024-02-20'
AND publish_datetime BETWEEN '2023-07-01' AND '2024-02-20';
