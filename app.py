from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Sample data
transactions = []

# Define usd filter
def usd(value):
    """Format value as USD."""
    return "${:,.2f}".format(value)

# Register usd filter in Jinja2 environment
app.jinja_env.filters['usd'] = usd

def calculate_total_money(transactions, current_day):
    total_money = 0

    for transaction in transactions:
        start_day = transaction["start_day"]
        recurrence_frequency = transaction["recurrence_frequency"]
        num_occurrences = transaction["num_occurrences"]
        indefinite = transaction["indefinite"]

        # Check if the transaction is within the recurrence interval
        if indefinite or (current_day - start_day) % recurrence_frequency == 0:
            total_money += transaction["amount"] * num_occurrences

    return total_money

@app.route('/')
def index():
    current_day = 120  # Set your desired value for the current day
    total_money = calculate_total_money(transactions, current_day)
    return render_template('index.html', total_money=total_money)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_name = request.form['transaction_name']
    transaction_type = request.form['transaction_type']
    recurrence_frequency = int(request.form['recurrence_frequency'])
    num_occurrences = int(request.form['num_occurrences'])
    indefinite = 'indefinite' in request.form

    # Add logic to handle the form data and update the transactions list
    # For simplicity, we'll append the data to the transactions list
    transactions.append({
        "transaction_name": transaction_name,
        "transaction_type": transaction_type,
        "recurrence_frequency": recurrence_frequency,
        "num_occurrences": num_occurrences,
        "indefinite": indefinite,
        "start_day": 120,  # Set your desired start day
        # Add other fields as needed
    })

    return redirect('/')  # Redirect back to the index page

if __name__ == '__main__':
    app.run(debug=True)
