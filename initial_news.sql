SELECT 
    doc_id AS news_id,
    title,
    regexp_replace(
        regexp_replace(content, '<[^>]+>', ''), 
        '</[^>]+>', 
        ''
    ) AS content,
    cat_lv1,
    cat_lv2,
    tags AS keywords,
    url,
    event_date AS date
FROM etl_ettoday_news
WHERE event_date BETWEEN '$tx_date(, -210D)' AND '$tx_date()'
AND publish_datetime BETWEEN '$tx_date(, -210D)' AND '$tx_date()';
