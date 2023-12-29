import logging

import azure.functions as func

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics import TextDocumentInput

# function to analyze sentiment
def analyse_sentiment(input_text):
    # Connect to the Azure Linguistic Analysis Service
    key = "b667e53fee6b438ab41eda0987b3ecc8"
    endpoint = "https://squad2.cognitiveservices.azure.com/"
    credentials = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credentials)

    # Analyze sentiment
    documents = [TextDocumentInput(id="1", text=input_text)]
    response = client.analyze_sentiment(documents=documents)[0]
    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    overall_positive = response.confidence_scores.positive
    overall_neutral = response.confidence_scores.neutral
    overall_negative = response.confidence_scores.negative
    if overall_positive > overall_negative and overall_positive > overall_neutral:
        return "positive"
    elif overall_positive < overall_negative and overall_negative > overall_neutral:
        return "negative"
    else:
        return "neutral"

def main(documents: func.DocumentList) -> str:
    logging.info('Document review => : %s', documents[0]['review_text'])
    logging.info('Analyse sentiment = > : %s', analyse_sentiment((documents[0]['review_text'])))
    
    return analyse_sentiment((documents[0]['review_text']))
