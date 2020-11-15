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
    input_symbol = request.form["Symbol"]
    info_center = StockInfoCenter(input_symbol)
    symbol_msg_info = info_center.tell_me()
    profile = symbol_msg_info.get("profile")
    recent_years = symbol_msg_info.get("Recent five years")
    average_price = symbol_msg_info.get("Average price")
    log.i(profile)
    log.i(recent_years)
    log.i(average_price)
    return render_template("home.html",
                           input_symbol=input_symbol,
                           tb1=profile.to_html(header=True,
                                               index=None,
                                               justify="center",
                                               table_id="table1"),
                           tb2=recent_years.to_html(header=True,
                                                    table_id="table2"),
                           tb3=average_price.to_html(header=True,
                                                     table_id="table3"))


if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)
