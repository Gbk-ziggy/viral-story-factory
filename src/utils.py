import os
import requests
import logging

def download_sample_background(output_folder):
    """Downloads a sample background video if the folder is empty."""
    os.makedirs(output_folder, exist_ok=True)
    
    # Check if folder is empty
    if not any(f.endswith(('.mp4', '.mov', '.mkv')) for f in os.listdir(output_folder)):
        logging.info("Assets folder is empty. Downloading sample background video...")
        
        # Example: A public domain or sample video URL
        # Using a reliable sample video URL
        url = "https://v.ftcdn.net/02/10/72/31/700_F_210723143_O08L69G9lB9vK9vK9vK9vK9vK9vK9vK9.mp4" # This is a placeholder, might not work
        # Let's use a more reliable one or just a placeholder message
        
        # Actually, let's use a reliable placeholder service if possible, 
        # but most are for images. 
        # For now, I'll use a direct link to a known sample file.
        sample_url = "https://www.w3schools.com/html/mov_bbb.mp4"
        
        try:
            response = requests.get(sample_url, stream=True, timeout=10)
            if response.status_code == 200:
                file_path = os.path.join(output_folder, "sample_background.mp4")
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                logging.info(f"Sample background downloaded to {file_path}")
                return file_path
            else:
                logging.error(f"Failed to download sample video. Status code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error downloading sample video: {e}")
    
    return None
