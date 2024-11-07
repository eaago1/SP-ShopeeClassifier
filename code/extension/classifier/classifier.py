from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import tfidf_lg_fn
import pandas as pd
import re
import requests
import csv
import scraper

app = Flask(__name__)
CORS(app)

@app.route("/")
def main_page():
    return "Send your POST request to /classify!"

@app.route("/total", methods=['POST'])
def get_total():
    data = request.json
    url = data['url']

    r = re.search(r'i\.(\d+)\.(\d+)', url)
    
    shop_id, item_id = r[1], r[2]
    ratings_url = 'https://shopee.ph/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset=0&shopid={shop_id}&type=0'

    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    data = requests.get(ratings_url.format(shop_id=shop_id, item_id=item_id), headers=headers).json()
    summary = data['data'].get('item_rating_summary', [])
    ratings = data['data'].get('ratings', [])
    item_desc = ratings[0].get('product_items',[])
    name = item_desc[0].get('name')
    total = {'total': summary.get('rating_total'), 'with_context': summary.get('rcount_with_context'), 'name': name}
    
    return jsonify(total)


@app.route("/scraper", methods=['POST'])
def scrape():
    data = request.json
    url = data['url']

    success = scraper.scrape_to_csv(url)
    
    return jsonify({'success': success})


@app.route('/classify', methods=['GET'])
def classify():
    tfidf_lg_fn.classifier()
    print("Classifying reviews completed.\n")
    
    df_with_labels = pd.read_csv('shopee_comments_with_labels.csv')
    
    positive_count = (df_with_labels['label'] == 1).sum()
    negative_count = (df_with_labels['label'] == 0).sum()
    
    total_reviews = len(df_with_labels)
    positive_percentage = (positive_count / total_reviews) * 100
    negative_percentage = (negative_count / total_reviews) * 100
    
    if positive_percentage <= 25:
        quality_category = "Poor Quality and Possibly Fraudulent"
    elif 25 < positive_percentage <= 40:
        quality_category = "Below Average Quality"
    elif 40 < positive_percentage <= 60:
        quality_category = "Average Quality"
    elif 60 < positive_percentage <= 80:
        quality_category = "Above Average Quality"
    elif 80 < positive_percentage <= 95:
        quality_category = "Excellent Quality and Legitimate Product"
    else:
        quality_category = "Excellent Quality with Caution on Legitimacy of Product"
        
    response = {
        'total_count': int(int(positive_count) + int(negative_count)),
        'positive_count': int(positive_count),
        'negative_count': int(negative_count),
        'positive_percentage': float(positive_percentage),     
        'negative_percentage': float(negative_percentage),
        'quality_category': quality_category
    }
    
    return jsonify(response)

@app.route("/download")
def download():
    file_path = "shopee_comments_with_labels.csv"
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
    new_filename = f"classification-{current_datetime}.csv"  
    return send_file(file_path, as_attachment=True, download_name=new_filename)

if __name__ == '__main__':
    app.run(debug=True)
