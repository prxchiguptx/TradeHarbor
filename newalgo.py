import pandas as pd
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

app = Flask(__name__)

# Function to fetch real-time stock price for a given ticker and exchange
def get_real_time_price(ticker, exchange):
    url = f'https://www.google.com/finance/quote/{ticker}:{exchange}?hl=en'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the element containing the price
        price_element = soup.find(class_="YMlKec fxKbKc")
        # Check if the element is found
        if price_element:
            price = float(price_element.text.strip()[1:].replace(",", ""))
            return price
        else:
            return None  # Element not found, return None
    else:
        return None  # Error fetching the webpage, return None


# Update the CSV file with real-time stock prices before rendering
def update_csv():
    data = pd.read_csv("testc.csv")
    for index, row in data.iterrows():
        ticker = row['Symbol']
        exchange = 'NSE'  # Assuming all stocks are from the same exchange
        real_time_price = get_real_time_price(ticker, exchange)
        if real_time_price is not None:
            data.at[index, 'CMP'] = real_time_price
    data.to_csv("testc.csv", index=False)


# Route to handle stock evaluation with real-time prices
def evaluate_stock(debt, market_cap, revenue, profit_margin, roa):
    debt_ranges = {
        "Very Low": (0, 10),
        "Low": (10, 30),
        "Medium": (30, 50),
        "High": (50, 70),
        "Very High": (70, float('inf'))
    }
 
    revenue_ranges = {
        "Very Low": (0, 2),
        "Low": (2, 5),
        "Medium": (5, 10),
        "High": (10, 20),
        "Very High": (20, float('inf'))
    }


    profit_margin_ranges = {
        "Very Low": (0, 5),
        "Low": (5, 10),
        "Medium": (10, 20),
        "High": (20, 30),
        "Very High": (30, float('inf'))
    }


    roa_ranges = {
        "Very Low": (0, 5),
        "Low": (5, 10),
        "Medium": (10, 20),
        "High": (20, 30),
        "Very High": (30, float('inf'))
    }


    # Evaluate each parameter based on its range
    debt_evaluation = evaluate_parameter(debt, debt_ranges)
    revenue_evaluation = evaluate_parameter(revenue, revenue_ranges)
    profit_margin_evaluation = evaluate_parameter(profit_margin, profit_margin_ranges)
    roa_evaluation = evaluate_parameter(roa, roa_ranges)
    
   
    # Return the overall evaluation based on the lowest evaluation among parameters
    evaluation = min(debt_evaluation, revenue_evaluation, profit_margin_evaluation, roa_evaluation)
    return evaluation


def evaluate_pe_ratio(pe_ratio):
    if pe_ratio < 20:
        return "Very Good"
    elif 20 <= pe_ratio < 25:
        return "Good"
    elif 25 <= pe_ratio < 30:
        return "Medium"
    elif 30 <= pe_ratio < 40:
        return "Low"
    else:
        return "Very Low"


def evaluate_parameter(value, ranges):
    for category, (lower, upper) in ranges.items():
        if lower <= value < upper:
            return category
    return "Undefined"


def load_company_data(company_name):
    # Load CSV data (Replace "your_file.csv" with the path to your CSV file)
    data = pd.read_csv(r"C:\Users\lenovo\OneDrive\Desktop\Practicumfinal\testc.csv")

    # Example attribute values for the specified company
    market_cap = data[data['Name'] == company_name]['MarketCap'].values[0]
    debt = data[data['Name'] == company_name]['DebtAmount'].values[0]
    revenue = data[data['Name'] == company_name]['Revenue'].values[0]
    profit_margin = data[data['Name'] == company_name]['Profit'].values[0]
    roa = data[data['Name'] == company_name]['Assets'].values[0]

    return market_cap, debt, revenue, profit_margin, roa


@app.route('/')
def Practicum():
    return render_template('Practicum.html')

@app.route('/FV')
def FV():
    return render_template('FV.html')

@app.route('/CMP')
def CMP():
    return render_template('CMP.html')


@app.route('/MC')
def MC():
    return render_template('MC.html')

@app.route('/BV')
def BV():
    return render_template('BV.html')


@app.route('/PTBV')
def PTBV():
    return render_template('PTBV.html')

@app.route('/IPE')
def IPE():
    return render_template('IPE.html')

@app.route('/DY')
def DY():
    return render_template('DY.html')


@app.route('/SC')
def SC():
    return render_template('SC.html')

@app.route('/NOS')
def NOS():
    return render_template('NOS.html')

@app.route('/RnS')
def RnS():
    return render_template('RnS.html')

@app.route('/TD')
def TD():
    return render_template('TD.html')

@app.route('/TR')
def TR():
    return render_template('TR.html')

@app.route('/PBDTEBDTA')
def PBDTEBDTA():
    return render_template('PBDTEBDTA.html')

@app.route('/PBDITPS')
def PBDITPS():
    return render_template('PBDITPS.html')

@app.route('/NETPROFITPERSHARE')
def NETPROFITPERSHARE():
    return render_template('NETPROFITPERSHARE.html')

@app.route('/NETPROFIT')
def NETPROFIT():
    return render_template('NETPROFIT.html')

@app.route('/CR')
def CR():
    return render_template('CR.html')

@app.route('/DER')
def DER():
    return render_template('DER.html')

@app.route('/RETURNONEQUITY')
def RETURNONEQUITY():
    return render_template('RETURNONEQUITY.html')

@app.route('/RETURNONASSETS')
def RETURNONASSETS():
    return render_template('RETURNONASSETS.html')

@app.route('/INTERESTCOVERAGERATIO')
def INTERESTCOVERAGERATIO():
    return render_template('INTERESTCOVERAGERATIO.html')

@app.route('/DIVIDENDPAYOUTRATIO')
def DIVIDENDPAYOUTRATIO():
    return render_template('DIVIDENDPAYOUTRATIO.html')

@app.route('/WEEKHL')
def WEEKHL():
    return render_template('WEEKHL.html')

@app.route('/VOLATILITYRATIO')
def VOLATILITYRATIO():
    return render_template('VOLATILITYRATIO.html')


@app.route('/index')
def index():
    return render_template('index.html')




@app.route('/evaluate')
def evaluate():
    # Define evaluation ranges
    debt_ranges = {
        "Very Low": (0, 10),
        "Low": (10, 30),
        "Medium": (30, 50),
        "High": (50, 70),
        "Very High": (70, float('inf'))
    }
 
    revenue_ranges = {
        "Very Low": (0, 2),
        "Low": (2, 5),
        "Medium": (5, 10),
        "High": (10, 20),
        "Very High": (20, float('inf'))
    }

    profit_margin_ranges = {
        "Very Low": (0, 5),
        "Low": (5, 10),
        "Medium": (10, 20),
        "High": (20, 30),
        "Very High": (30, float('inf'))
    }

    roa_ranges = {
        "Very Low": (0, 5),
        "Low": (5, 10),
        "Medium": (10, 20),
        "High": (20, 30),
        "Very High": (30, float('inf'))
    }

    # Get the company name from the URL parameter
    company_name = request.args.get('company')

    # Read data from testc.csv to get the URL
    testc_data = pd.read_csv('testc.csv')

    # Find the row corresponding to the clicked company
    company_row = testc_data[testc_data['Name'] == company_name]

    if not company_row.empty:
        # Get the URL from the row
        csv_url = company_row['url'].iloc[0]

        # Read data from the CSV file specified by the URL
        data = pd.read_csv(csv_url)

        # Plot line chart
        plt.figure(figsize=(10, 5))
        plt.plot(data['Date'], data['Price'], marker='o', linestyle='-', color='green')  # Green line color
        plt.xlabel('Date', color='white')  # White x-axis label color
        plt.ylabel('Price', color='white')  # White y-axis label color
        plt.title(f'Stock Price Over Time - {company_name}', color='white')  # White title color
        plt.xticks(rotation=45, color='white')  # Rotate x-axis labels for better readability
        plt.yticks(color='white')  # White color for y-axis ticks
        plt.gca().spines['bottom'].set_color('white')  # White color for x-axis spine
        plt.gca().spines['left'].set_color('white')  # White color for y-axis spine
        plt.gca().set_facecolor((0, 0, 0, 0.5))  # Transparent black background
        plt.grid(False)  # Remove grid lines
        plt.tight_layout()

        # Save the plot as an image
        image_path = os.path.join('static', 'stock_price_chart.png')
        plt.savefig(image_path, transparent=True)  # Save with transparent background
        plt.close()

        # Get the company name from the URL parameter
        company_name = request.args.get('company')
        # Load data for the specified company
        data = pd.read_csv("testc.csv")
        update_csv()  # Update CMP before evaluation
        market_cap = data[data['Name'] == company_name]['MarketCap'].values[0]
        debt = data[data['Name'] == company_name]['DebtAmount'].values[0]
        revenue = data[data['Name'] == company_name]['Revenue'].values[0]
        profit_margin = data[data['Name'] == company_name]['Profit'].values[0]
        roa = data[data['Name'] == company_name]['Assets'].values[0]
        cmp = data[data['Name'] == company_name]['CMP'].values[0]  # Get real-time CMP
        pe_ratio = data[data['Name'] == company_name]['PE'].values[0]

        # Load data for the specified company
        market_cap, debt, revenue, profit_margin, roa = load_company_data(company_name)

        # Evaluate the stock for the specified company
        potential = evaluate_stock(debt, market_cap, revenue, profit_margin, roa)

        # Render the result template with the computed potential
        return render_template('resultnew.html', CName=company_name, 
                               debtevaluation=evaluate_parameter(debt, debt_ranges),
                               revenueevaluation=evaluate_parameter(revenue, revenue_ranges),
                               profitmarginevaluation=evaluate_parameter(profit_margin, profit_margin_ranges),
                               roaevaluation=evaluate_parameter(roa, roa_ranges),
                               potential=potential,
                               market_cap=market_cap,
                               debt=debt,
                               revenue=revenue,
                               profit_margin=profit_margin,
                               roa=roa, current_market_price=cmp,
                               peevaluation=evaluate_pe_ratio(pe_ratio), peratio=pe_ratio)
    else:
        return "Company not found"

if __name__ == '__main__':
    app.run(debug=True, port=8080)
