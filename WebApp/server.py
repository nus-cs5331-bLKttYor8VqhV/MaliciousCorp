from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/form.html')
def form():
    return render_template("form.html")

@app.route('/sgx/form', methods=["POST"])
def post():
    if request.method == 'POST':
        user_name = request.form['name']
        card_number = request.form['card_num']
        month = request.form['month']
        year = request.form['year']
        cvc_code = request.form['cvc']
        print(user_name)

    return render_template("form.html")
    
if __name__ == '__main__':
    app.debug = True 
    app.run(ssl_context='adhoc')
