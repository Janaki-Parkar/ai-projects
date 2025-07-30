from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

def get_sentiment(polarity):
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        blob = TextBlob(text)
        polarity = round(blob.polarity, 2)
        subjectivity = round(blob.subjectivity, 2)
        sentiment = get_sentiment(polarity)
        return render_template('index1.html', text=text, polarity=polarity, subjectivity=subjectivity, sentiment=sentiment)
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)