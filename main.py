from fastapi import FastAPI
from pydantic import BaseModel
from utils import authenticate_client
from dotenv import load_dotenv
import os
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

load_dotenv()

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(10)
logger.addHandler(AzureLogHandler(
    connection_string=os.getenv("INSTRUNENTATION_KEY")))


class Model(BaseModel):
    text_to_analyze: list


@app.post("/")
def sentiment_analysis_example(documents: Model):
    """[summary]

    Args:
        documents (Model): [description]

    Returns:
        [type]: [description]
    """

    client = authenticate_client()

    response_dict = {}

    for idx, document in enumerate(documents.text_to_analyze):
        response = client.analyze_sentiment(
            documents=documents.text_to_analyze)

        response_dict[response[idx]["id"]] = {
            "sentiment": response[idx]["sentiment"],
            "confidence_scores": response[idx]["confidence_scores"],
            "sentences": [sentence["text"] for sentence in response[idx]["sentences"]]
        }

        log_data = {
            "custom_dimensions":
            {
                "text_sentiment":  response[idx]["sentiment"]
            }
        }
        logger.info('Text Processed Succesfully', extra=log_data)

    return response_dict

    # [
    #     {
    #         "id": "0",
    #         "sentiment": "mixed",
    #         "warnings": [],
    #         "statistics": null,
    #         "confidence_scores": {
    #             "positive": 0.5,
    #             "neutral": 0,
    #             "negative": 0.5
    #         },
    #         "sentences": [
    #             {
    #                 "text": "I think this is super cool.",
    #                 "sentiment": "positive",
    #                 "confidence_scores": {
    #                     "positive": 1,
    #                     "neutral": 0,
    #                     "negative": 0
    #                 },
    #                 "length": 27,
    #                 "offset": 0,
    #                 "mined_opinions": []
    #             },
    #             {
    #                 "text": "But not as cool as you.",

    # print("Document Sentiment: {}".format(response.sentiment))
    # print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
    #     response.confidence_scores.positive,
    #     response.confidence_scores.neutral,
    #     response.confidence_scores.negative,
    # ))
    # for idx, sentence in enumerate(response.sentences):
    #     print("Sentence: {}".format(sentence.text))
    #     print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
    #     print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
    #         sentence.confidence_scores.positive,
    #         sentence.confidence_scores.neutral,
    #         sentence.confidence_scores.negative,
    #     ))


# def analyze_text(text: Model):
#     response = {
#         "sentiment": [],
#         "keyphrases": []
#     }
#     no_of_text = len(text.text_to_analyze)
#     for i in range(no_of_text):
#         document = {
#             "documents": [
#                 {
#                     "id": i+1,
#                     "language": "en",
#                     "text": text.text_to_analyze[i]
#                 }
#             ]
#         }
#         sentiment = utils.call_text_analytics_api(
#             headers, document, endpoint='sentiment')
#         keyphrases = utils.call_text_analytics_api(
#             headers, document, endpoint='keyPhrases')
#         response["sentiment"].append(sentiment["documents"][0])
#         response["keyphrases"].append(keyphrases["documents"][0])
# return response
