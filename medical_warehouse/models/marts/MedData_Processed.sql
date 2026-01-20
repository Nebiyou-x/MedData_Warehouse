{{config(materialized='table')}}

-- / Removing white spaces for the messages column

WITH clean_data as (
    SELECT 
        TRIM(message) AS message_cleaned, *
    FROM {{ref('MedData_cleaned')}}
)


SELECT 
    channel_username,
    message_cleaned,
    date,
    media_path,
    ID

FROM clean_data