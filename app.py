from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        result = float(request.form['a']) + float(request.form['b'])
    return render_template('index.html', result=result)


## CALCULATOR PAGE ROUTE
@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    return render_template("calculator.html")



if __name__ == '__main__':
    app.run(debug=True, port=5001)
