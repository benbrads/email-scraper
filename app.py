from flask import Flask, request, jsonify
from scraper import scrape_site_for_facebook, parse_facebook_for_email, scrape_site_for_email

app = Flask(__name__)

@app.route('/email', methods=['POST'])
def scrape():
    url = request.json['url']
    email = ""
    if "facebook" in url:
        email = parse_facebook_for_email(url)
    else:
        facebook_link = scrape_site_for_facebook(url)
        if(facebook_link == ""):
            email = scrape_site_for_email(url)
        else:
            email = parse_facebook_for_email(facebook_link)
    data = {"email": email}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
