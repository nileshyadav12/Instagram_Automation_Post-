import requests
import logging
import json

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

class InstagramAutomation:
    def __init__(self, config, caption, image_path):
        """Initializes the InstagramAutomation class using configuration data and hardcoded caption/image path."""
        # Use the configuration values passed to the constructor
        self.access_token = config.get('access_token')
        self.page_id = config.get('page_id')
        self.instagram_account_id = config.get('instagram_account_id')
        self.caption = caption  # Caption is now passed directly in the constructor
        self.image_path = image_path  # Image path is now passed directly in the constructor
        self.imgur_client_id = config.get('imgur_client_id')

    def upload_image_to_imgur(self):
        """Uploads an image to Imgur and returns the image URL."""
        url = 'https://api.imgur.com/3/upload'
       
        # Open the image file
        with open(self.image_path, 'rb') as image_file:
            headers = {'Authorization': f'Client-ID {self.imgur_client_id}'}
            files = {'image': image_file}
            response = requests.post(url, headers=headers, files=files)
 
        if response.status_code == 200:
            # Extract the URL of the uploaded image from the response
            image_url = response.json()['data']['link']
            logging.info(f"Image uploaded successfully! Image URL: {image_url}")
            return image_url
        else:
            logging.error("Failed to upload image.")
            return None

    def create_instagram_post(self):
        """Creates a post on Instagram using the Instagram Graph API."""
        # Step 1: Upload image to Imgur and get the URL
        imgur_url = self.upload_image_to_imgur()
        if not imgur_url:
            raise Exception("Failed to get image URL from Imgur.")
 
        # Step 2: Upload the image to Instagram
        url = f"https://graph.facebook.com/v15.0/{self.instagram_account_id}/media"
        params = {
            'image_url': imgur_url,
            'caption': self.caption,  # Caption is passed directly
            'access_token': self.access_token
        }
       
        response = requests.post(url, params=params)
       
        if response.status_code == 200:
            media_id = response.json().get('id')
            logging.info(f"Successfully uploaded image to Instagram. Media ID: {media_id}")
           
            # Step 3: Publish the post on Instagram
            publish_url = f"https://graph.facebook.com/v21.0/{self.instagram_account_id}/media_publish"
            publish_params = {
                'creation_id': media_id,
                'access_token': self.access_token
            }
           
            publish_response = requests.post(publish_url, params=publish_params)
 
            if publish_response.status_code == 200:
                logging.info("Successfully published post on Instagram!")
            else:
                logging.error(f"Error publishing post: {publish_response.text}")
        else:
            logging.error(f"Error uploading image to Instagram: {response.text}")


def load_config(config_file):
    """Loads configuration from the JSON file."""
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        logging.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise


if __name__ == "__main__":
    try:
        # Load configuration from JSON file
        config = load_config(rf'C:\Users\User\Desktop\deep\inatagram image post\confiq.json')

        # Hardcoded caption and image path
        caption = "This is my Instagram caption!"
        image_path = rf"C:\Users\User\Desktop\deep\inatagram image post\images\d1.jpg"

        # Initialize the Instagram automation class with the loaded config and the caption/image path
        automation = InstagramAutomation(config, caption, image_path)
        automation.create_instagram_post()

    except Exception as e:
        logging.error(f"An error occurred: {e}")



