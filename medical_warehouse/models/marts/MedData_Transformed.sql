{{config(materialized='table')}}


WITH Processed_data AS (
    SELECT *
    From {{ref('MedData_Processed')}}
    WHERE channel_username = '@lobelia4cosmetics'
)


SELECT
    SUBSTRING(message_cleaned 
        FROM POSITION('^[a-zA-Z]+$' IN message_cleaned)
        FOR POSITION('Price ' IN message_cleaned) - POSITION('^[a-zA-Z]+$' IN message_cleaned)) AS Product,

    SUBSTRING(message_cleaned 
        FROM POSITION('Price ' IN message_cleaned) + LENGTH('Price ')
        FOR POSITION(' birr' IN message_cleaned) - POSITION('Price ' IN message_cleaned)) AS Price,


    SUBSTRING(message_cleaned 
        FROM POSITION('Adress:- ' IN message_cleaned) + LENGTH('Adress:- ')
        FOR POSITION('Open' IN message_cleaned) - POSITION('Adress:- ' IN message_cleaned)) AS Address,  


    SUBSTRING(message_cleaned 
        FROM POSITION('call ' IN message_cleaned) + LENGTH('call ')
        FOR POSITION('Adress' IN message_cleaned) - POSITION('call ' IN message_cleaned)) AS Phone_number, *

FROM Processed_data

