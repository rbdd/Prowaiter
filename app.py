from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

waitlist = []

@app.route('/')
def home():
    return render_template('home.html', waitlist=waitlist)

@app.route('/add_to_waitlist', methods=['POST'])
def add_to_waitlist():
    customer_name = request.form.get('customer_name')

    if customer_name:
        waitlist.append(customer_name)
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
