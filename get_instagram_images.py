import requests
import json
import re
import os
from urllib.parse import urljoin

def get_instagram_images(username, max_images=12):
    """Get Instagram images from a public profile"""
    
    # Instagram URL
    url = f"https://www.instagram.com/{username}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Look for JSON data in the page
            pattern = r'window\._sharedData = ({.+?});'
            match = re.search(pattern, response.text)
            
            if match:
                data = json.loads(match.group(1))
                
                # Navigate through the JSON structure to find images
                try:
                    user = data['entry_data']['ProfilePage'][0]['graphql']['user']
                    media = user['edge_owner_to_timeline_media']['edges']
                    
                    images = []
                    for i, item in enumerate(media[:max_images]):
                        node = item['node']
                        if node['__typename'] == 'GraphImage':
                            image_url = node['display_url']
                            images.append(image_url)
                        elif node['__typename'] == 'GraphSidecar':
                            # For carousel posts, get the first image
                            if node.get('edge_sidecar_to_children'):
                                first_child = node['edge_sidecar_to_children']['edges'][0]['node']
                                if first_child['__typename'] == 'GraphImage':
                                    image_url = first_child['display_url']
                                    images.append(image_url)
                    
                    return images
                    
                except KeyError as e:
                    print(f"Error parsing Instagram data: {e}")
                    return []
            else:
                print("Could not find Instagram data")
                return []
        else:
            print(f"Failed to fetch Instagram page: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching Instagram: {e}")
        return []

def download_images(image_urls, folder="instagram_images"):
    """Download images from URLs"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    downloaded = []
    for i, url in enumerate(image_urls):
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
    print(f"Fetching images from @{username}...")
    
    images = get_instagram_images(username)
    
    if images:
        print(f"Found {len(images)} images")
        downloaded = download_images(images)
        print(f"Downloaded {len(downloaded)} images to instagram_images/")
    else:
        print("No images found or unable to access profile")