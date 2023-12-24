import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency'] 
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    
    # Get just string without quotes 
    target_currency = data['queryResult']['parameters']['currency-name'][0]

    cf = fetch_conversion_factor(source_currency, target_currency)
    
    if cf is None:
        response = {
            "fulfillmentText": "Sorry, unable to get conversion rate."
        }
        return jsonify(response)
        
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    
    response = {
        "fulfillmentText": "{} {} is {} {}".format(amount, source_currency, 
                                                   final_amount, target_currency)
    }
    
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=af9fe87465f485e7013a".format(source, target)
    response = requests.get(url)
    
    try:
        return response.json()['{}_{}'.format(source, target)]
    except KeyError: 
        return None

if __name__ == "__main__":
    app.run(debug=True)
