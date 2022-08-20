import bleach
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def editor():
    return render_template('index.html')

@app.route('/display', methods = ['GET', 'POST'])
def display():
    if request.method == 'POST':
        content = request.form.get('content')
        print(content)
        return render_template('display.html', content = content)

if __name__ == "__main__":
    app.run()
