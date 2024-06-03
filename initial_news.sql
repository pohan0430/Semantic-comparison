WITH user_view_news AS (
    SELECT et_token_hash AS et_token, news_id AS news_id
    FROM etl_custom_tag_autokeyword_audience_count_user_base
),
news_keywords AS (
    SELECT news.id AS id, news.news_keywords AS keywords
    FROM etl_custom_tag_autokeyword_audience_count_news_base AS news
),
joined_data AS (
    SELECT uvn.et_token, nk.id AS news_id, nk.keywords
    FROM user_view_news uvn
    JOIN news_keywords nk ON uvn.news_id = nk.id
),
audience_count AS (
    SELECT news_id, COUNT(DISTINCT et_token) AS audience_size
    FROM joined_data
    GROUP BY news_id
),
ettoday_news AS (
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
        event_date AS date,
        img
    FROM etl_ettoday_news
    WHERE event_date BETWEEN '$tx_date(, -210D)' AND 'tx_date()'
    AND publish_datetime BETWEEN '$tx_date(, -210D)' AND 'tx_date()'
)
SELECT en.news_id, en.title, en.content, en.cat_lv1, en.cat_lv2, en.keywords, en.url, en.date, en.img, COALESCE(ac.audience_size, 0) AS audience_size
FROM ettoday_news en
LEFT JOIN audience_count ac ON TRIM(en.news_id) = TRIM(ac.news_id)