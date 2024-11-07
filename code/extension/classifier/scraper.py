import re
import requests
import csv

def scrape_to_csv(url):
    r = re.search(r'i\.(\d+)\.(\d+)', url)  
    
    shop_id, item_id = r[1], r[2]
    ratings_url = 'https://shopee.ph/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset={offset}&shopid={shop_id}&type=0'

    print("\nSHOP ID: ", shop_id,"\nITEM ID: ", item_id)
    
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    offset = 0

    with open('shopee_comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            data = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id, offset=offset), headers=headers).json()
            print("OFFSET: ", offset)
            if 'data' in data:
                ratings = data['data'].get('ratings', [])  # Get ratings or empty list (if null)
            
                if ratings:  
                    repeat = 0 # Checks if an offset set are all repeating if this reaches 20
                    for rating in ratings:
                        comment = rating.get('comment', '')  # Get the comment, or empty string if comment is None
                        if repeat == 19: 
                            return 1
                        elif comment:
                            comment = comment.replace('\n', ' ')  # Replace newline characters with space
                            writer.writerow({'text': comment})
                        elif not comment and not rating.get('images') and not rating.get('videos'):
                            repeat = repeat + 1
                else:
                    break  # Exit loop if ratings are null or empty list

                if len(ratings) < 20:
                    break

                offset += 20
            else:
                print("Data not found. Retrying...")

    return 1