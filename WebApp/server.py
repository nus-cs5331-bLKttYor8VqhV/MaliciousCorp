from flask import Flask, render_template, request, redirect, url_for
from interface import EnclaveRequest
import time
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


@app.route('/sgx/form', methods=["POST"])
def post():
    user_name = request.form['name']
    card_number = request.form['card_num']
    month = request.form['month']
    year = request.form['year']
    cvc_code = request.form['cvc']

    try:
        a = EnclaveRequest()
        data = {"user_name": user_name,
        "card_number": card_number,
        "month": month,
        "year": year,
        "cvc_code": cvc_code
        }
        answ = a.post("https://httpbin.org/post", data)
        print(answ.content)
        print(answ.get_dict_from_content())
        ok_condition = True # TODO
        if ok_condition:
            return redirect(url_for('accepted'))
        else:
            return redirect(url_for('refused'))
    except:
        print("problem")
        return redirect(url_for('refused'))

@app.route('/sgx/key_exchange',methods=['POST'])
def key_exchange():
    public_key = request.form['public_key']
    q = request.form['q']
    a = request.form['a']
    
    try:
        p = EnclaveRequest()
        data = {"public_key": public_key,
        "q": q,
        "a": a
        }
        answ = p.post("https://key_exchange/post", data)
        print(answ.content)
        print(answ.get_dict_from_content())
        return answ
    except:
        print("problem")
        return redirect(url_for('refused'))

if __name__ == '__main__':
    app.debug = True 
    app.run(ssl_context='adhoc')
