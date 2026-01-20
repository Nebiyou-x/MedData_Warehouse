import os
import logging
import demoji
import json

from dotenv import load_dotenv
from telethon import TelegramClient
from database import DbConn



class Cache:
    
    def __init__(self):
        '''
        This class contains the logic of caching the data that is scraped so that re-scraping won't happen
        '''
        self.CACHE_FILE = 'data/scraped_message_id.json'

    def load_cache(self):
        '''
        A function to load the caches
        '''
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, 'r') as file:
                return json.load(file)  
        return {}  


    def save_cache(self, data):
        '''
        A function to save caches
        '''
        with open(self.CACHE_FILE, 'w') as file:  
            json.dump(data, file)



class Util:
    def __init__(self):
        self.logger = self.logger_setup()
        self.dbConn = DbConn()
        self.cache = Cache()


    def logger_setup(self):
        '''
        This funciton is used to setup logging
        '''
        log_dir = os.path.join(os.getcwd(), 'logs')

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        log_file_info = os.path.join(log_dir, 'Info.log')
        log_file_error = os.path.join(log_dir, 'Error.log')

        formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s',
                                    datefmt='%Y-%m-%d %H:%M')

        info_handler = logging.FileHandler(log_file_info)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        error_handler = logging.FileHandler(log_file_error)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)
        # console_handler.setFormatter(formatter)


        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)
        # logger.addHandler(console_handler)       

        return logger 
    

    def remove_emoji(self, text):
        '''
        This function removes the emoji from text

        Parameter:
        ---------
            text(str): text with emojis
        
        Return:
        -------
            text(str): text without emojis
        '''
        try:
            no_emoji = demoji.replace(text, repl = "")
        except:
            no_emoji = text

        return no_emoji
    

    def setup_telegram_client(self):
        '''
        This function creates a telegram client 
        '''
        load_dotenv('.env')
        api_id = os.getenv('TG_API_ID')
        api_hash = os.getenv('TG_API_HASH')
        return TelegramClient('scraping_session', api_id, api_hash) 


    async def scrape_channel(self, client, channel_username, writer, media_dir, cache):
        try:
            entity = await client.get_entity(channel_username)
            channel_title = entity.title  

            async for message in client.iter_messages(entity, limit=10000):
                
                try:
                    if message.id in cache[channel_username]:
                        continue
                except:
                    self.logger.info(f"Scraping new Channel {channel_username}")
                    cache[channel_username] = []

                media_path = None
                if message.media:
                    # Create a unique filename for the photo
                    filename = f"{channel_username}_{message.id}.{message.media.document.mime_type.split('/')[-1]}" if hasattr(message.media, 'document') else f"{channel_username}_{message.id}.jpg"
                    media_path = os.path.join(media_dir, filename)
                    # Download the media to the specified directory if it's a photo
                    await client.download_media(message.media, media_path)
                    self.logger.info(f"Downloaded media for message ID {message.id}.")
                
                
                writer.writerow([channel_title, channel_username, message.id, self.remove_emoji(message.message), message.date, media_path])
                self.logger.info(f"saved message ID {message.id} from {channel_username} to csv format.")
                self.dbConn.insert_data(channel_title, channel_username, message.id, self.remove_emoji(message.message), message.date, media_path)
                self.logger.info(f"saved message ID {message.id} from {channel_username} to database.")
                self.logger.info(f"Processed message ID {message.id} from {channel_username}.")
                
                cache[channel_username].append(message.id)


                self.cache.save_cache(cache)
        except Exception as e:
            self.logger.error(f"Error while scraping {channel_username}: {e}")            
