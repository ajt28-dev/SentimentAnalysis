from flask import Flask, render_template, url_for, redirect, request, Response
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import emoji

app = Flask(__name__, template_folder='Templates', static_folder='static', static_url_path='/')

# Download necessary NLTK data
nltk.download('vader_lexicon')

# Create the sentiment analyzer outside any function
sia = SentimentIntensityAnalyzer()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def get_emoji(sentiment_score):
    if sentiment_score >= 0.8:  # Adjusted threshold for smiley
        return emoji.emojize(":smiling_face_with_smiling_eyes:")  #😊
    elif sentiment_score >= 0.2:  # Adjusted threshold for slightly smiling face
        return emoji.emojize(":slightly_smiling_face:")  #🙂
    elif sentiment_score > -0.2 and sentiment_score < 0.2:
        return emoji.emojize(":neutral_face:")  #😐
    elif sentiment_score < -0.8:  # Changed range for slightly frowning face
        return emoji.emojize(":slightly_frowning_face:")  #🙁
    else:
        return emoji.emojize(":angry_face:")  #😠

def analyze_text_with_emoji(text):
    sentiment = sia.polarity_scores(text)  # Get sentiment scores
    sentiment_score = sentiment['compound']  # Compound score for overall sentiment
    matched_emoji = get_emoji(sentiment_score)  # Get corresponding emoji
    return f"{text} {matched_emoji} (Score: {sentiment_score:.2f})"

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get text from the form
    text = request.form.get('text', '')
    
    # Use your analysis function
    result = analyze_text_with_emoji(text)
    
    # Get sentiment scores for detailed display
    sentiment = sia.polarity_scores(text)
    
    # Return the results to a results page
    return render_template('analyze.html', 
                          text=text, 
                          result=result,
                          sentiment_score=sentiment['compound'],
                          emoji=get_emoji(sentiment['compound']),
                          scores=sentiment)

if __name__ == '__main__':
    app.run(debug=True)