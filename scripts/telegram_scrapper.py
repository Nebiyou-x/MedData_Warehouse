import csv
import os
import asyncio
from database import DbConn
from Utils import Util, Cache

util = Util()
dbConn = DbConn()
caches = Cache()

logger = util.logger_setup()
client = util.setup_telegram_client()


async def main():
    await client.start()
    
    # Create a directory for media files
    media_dir = 'data/photos'
    os.makedirs(media_dir, exist_ok=True)

    # Open the CSV file and prepare the writer
    with open('data/telegram_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        cache = caches.load_cache()

        if os.stat('data/telegram_data.csv').st_size==0:
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
        
        channels = [
            '@DoctorsET',
            '@CheMed123',
            '@lobelia4cosmetics' ,
            '@yetenaweg',
            '@EAHCI',
            '@TikvahPharmacy',

        ]

        tasks = [util.scrape_channel(client, channel, writer, media_dir, cache) for channel in channels]

        await asyncio.gather(*tasks)

        logger.info("Scraping completed.")

with client:
    client.loop.run_until_complete(main())