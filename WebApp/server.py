from flask import Flask, render_template, request, redirect, url_for
from interface import EnclaveRequest
import time, traceback, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/form.html')
def form():
    return render_template("form.html")

@app.route('/accepted')
def accepted():
    return render_template("success.html")

@app.route('/refused')
def refused():
    return render_template("error.html")

@app.route('/sgx/key_exchange',methods=['POST'])
def key_exchange():
    x = request.json['x']
    y = request.json['y']
    try:
        p = EnclaveRequest()
        data = {"x": x, "y": y}
        print("Key Exchange, Browser public key : ", data)
        answ = p.post("https://key_exchange/post", data)
        print("Key Exchange, Server public key : ", answ.get_dict_from_content())
        return json.dumps(answ.get_dict_from_content())
    except:
        print("Error occured")
        return redirect(url_for('refused'))

@app.route('/sgx/form', methods=["POST"])
def post():
    enc = request.form['enc']
    iv = request.form['iv']
    
    try:
        a = EnclaveRequest()
        data = {
            "enc": enc,
            "iv": iv}
        answ = a.post("https://httpbin.org/post", data)
        print("\nAnswer from bank: ", answ.get_dict_from_content())
        ok_condition = True # If the format is wrong, the above line will throw an exception (get_dict_from_content), sufficient for the poc
        if ok_condition:
            return redirect(url_for('accepted'))
        else:
            return redirect(url_for('refused'))
    except:
        print("problem")
        return redirect(url_for('refused'))

if __name__ == '__main__':
    app.debug = True 
    app.run(ssl_context='adhoc')
