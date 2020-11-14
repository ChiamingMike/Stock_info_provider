from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

from infocenter.logger.Log import log
from infocenter.StockInfoCenter import StockInfoCenter


app = Flask(__name__)


@app.route("/")
def root():
    page_title = "Search"
    return render_template("home.html",
                           title=page_title)


@app.route('/search_result', methods=['GET', 'POST'])
def search_result():
    df = pd.DataFrame({"col1": ["val1", "val2", "val3"]}, index=[
                      "row1", "row2", "row3"])
    input_symbol = request.form["Symbol"]
    info_center = StockInfoCenter(input_symbol)
    symbol_msg_info = info_center.tell_me()
    profile = symbol_msg_info.get("profile")
    recent_five_years = symbol_msg_info.get("Recent five years")
    average_price = symbol_msg_info.get("Average price")
    log.i(profile)
    log.i(recent_five_years)
    log.i(average_price)
    return render_template("home.html",
                           input_symbol=input_symbol,
                           tb1=profile.to_html(header=True),
                           tb2=recent_five_years.to_html(header=True),
                           tb3=average_price.to_html(header=True))


if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)
