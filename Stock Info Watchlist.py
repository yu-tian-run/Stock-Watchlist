from flask import Flask, render_template, request, redirect, url_for, flash
from Utils import save_watchlist, load_watchlist, fetch_stock_data

app = Flask(__name__)
app.secret_key = "ABCDEFG"

@app.route("/", methods=["GET", "POST"])
def index():
    tickers = load_watchlist()
    if request.method == "POST":
        ticker = request.form.get("ticker").upper().strip()
        if not ticker:
            flash('Please enter a valid ticker symbol.', 'error')
        else:
            data = fetch_stock_data(ticker)
            if data:
                if ticker not in tickers:
                    tickers.append(ticker)
                    save_watchlist(tickers)
                    flash(f'{ticker} added.', 'success')
                else:
                    flash(f'{ticker} is already in your watchlist.', 'info')
            else:
                flash(f' Problem with {ticker}.', 'error')
            return redirect(url_for('index'))
    else: 
        stock_data = []
        for ticker in tickers:
            data = fetch_stock_data(ticker)
            if data:
                stock_data.append(data)

        return render_template('index.html', stocks = stock_data)



@app.route('/remove/<ticker>')
def remove(ticker):
    tickers = load_watchlist()
    if ticker in tickers:
        tickers.remove(ticker)
        save_watchlist(tickers)
        flash(f'{ticker} removed from watchlist.', 'success')
    else:
        flash(f'{ticker} is not in your watchlist.', 'error')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
