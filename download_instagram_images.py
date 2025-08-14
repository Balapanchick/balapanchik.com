import requests
import os
import json
from bs4 import BeautifulSoup
import re
import time

def get_instagram_images_simple(username, max_images=12):
    """Simple method to get Instagram images using web scraping"""
    
    url = f"https://www.instagram.com/{username}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            # Look for image URLs in the HTML
            image_pattern = r'(https?://[^\s"\']+\.jpg)'
            matches = re.findall(image_pattern, response.text)
            
            # Filter for Instagram CDN URLs
            instagram_images = [url for url in matches if 'instagram' in url and 'cdninstagram' in url]
            
            # Remove duplicates and take first max_images
            unique_images = list(set(instagram_images))[:max_images]
            
            return unique_images
        else:
            print(f"Failed to fetch page: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

def download_images_fallback():
    """Use placeholder images that match the theme"""
    
    # High-quality placeholder images for children's clothing
    placeholder_urls = [
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1474557157379-8aa74a6ef541?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1496661415325-ef852f9e8e7c?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1493770348161-369560ae357d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1516796181074-bf453fbfa3e6?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400&h=400&fit=crop"
    ]
    
    folder = "instagram_images"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    downloaded = []
    for i, url in enumerate(placeholder_urls):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"instagram_{i+1}.jpg"
                filepath = os.path.join(folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                downloaded.append(filepath)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download image {i+1}: {response.status_code}")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")
    
    return downloaded

if __name__ == "__main__":
    username = "balapanchikkz"
    print(f"Attempting to fetch images from @{username}...")
    
    # Try to get images from Instagram
    images = get_instagram_images_simple(username)
    
    if images:
        print(f"Found {len(images)} images from Instagram")
        # Download the images
        folder = "instagram_images"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        downloaded = []
        for i, url in enumerate(images):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    filename = f"instagram_{i+1}.jpg"
                    filepath = os.path.join(folder, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    downloaded.append(filepath)
                    print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Error downloading image {i+1}: {e}")
    else:
        print("Could not fetch Instagram images, using fallback images...")
        downloaded = download_images_fallback()
    
    print(f"Total images downloaded: {len(downloaded)}")