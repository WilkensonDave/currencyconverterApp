from flask import Flask, render_template, request, redirect
import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

# parameters = {"api_key": MY_API_KEY, "base_code":"EUR", "target_code":""}
# response = requests.get(url, params=parameters)
# data = response.json()

app = Flask(__name__)
@app.route("/", methods=["POST", "GET"])
def home():
    
    API = os.getenv("MY_API_KEY")
    URL=URL=f"https://v6.exchangerate-api.com/v6/{API}/codes"
    all_codes = requests.get(URL).json()
    codes = all_codes["supported_codes"]
    
    if request.method == "POST":
        url = f'https://v6.exchangerate-api.com/v6/{API}/latest/USD'
        response = requests.get(url)
        data = response.json()
        countries = data["conversion_rates"]
        
        class CurrencyConverter:
            def __init__(self, url):
                self.data = requests.get(url).json()
                self.currencies = self.data["conversion_rates"]
                
            def convert (self, basecurrency, tocurrency, amount):
                if basecurrency != "USD":
                    amount = float(amount) /float(self.currencies[basecurrency])
                amount = round(float(amount) * float(self.currencies[tocurrency]), 4)
                
                return amount
        
        basecurrency = request.form["basecurrency"]
        tocurrency = request.form["tocurrency"]
        amount = request.form["amount"]
        converter = CurrencyConverter(url)
        finalresult = converter.convert(basecurrency, tocurrency, amount)
        
        return render_template("index.html", 
                               basecurrency=basecurrency, tocurrency=tocurrency, 
                               amount=amount, finalresult=finalresult, countries=countries, codes=codes)
    
    
    url = f'https://v6.exchangerate-api.com/v6/{API}/latest/USD'
    data = requests.get(url).json()
    countries = data["conversion_rates"]
    
    return render_template("index.html", countries=countries, codes=codes)

    
if __name__ == "__main__":
    app.run(debug=True)

