
import pandas as pd
from transformers import pipeline

# Load the spreadsheet
df = pd.read_excel("RelevantTweets.xlsx", engine="openpyxl")

# Load BERT sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Apply sentiment analysis to each tweet
def analyze_sentiment(text):
    if pd.isna(text):
        return None
    result = sentiment_pipeline(text[:512])[0]  # Truncate to 512 tokens for BERT
    return f"{result['label']} ({result['score']:.2f})"

# Create a new column with sentiment results
df['BERT Sentiment'] = df['Tweets'].apply(analyze_sentiment)

# Save the updated spreadsheet
df.to_excel("RelevantTweets_Analyzed.xlsx", index=False)
print("Sentiment analysis completed and saved to RelevantTweets_Analyzed.xlsx.")
