import json
import requests
import bs4
import boto3
from contextlib import closing

def web_scraper(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    
    # Grab the url from the event json and grab the source file using requests
    url = event['url_search']
    response = requests.get(url)

    # convert the source html to a beautifulSoup object, select all <p> tags
    website_full_text = bs4.BeautifulSoup(response.text, features="lxml")
    # website_raw_text = website_full_text.select('p')
    website_raw_text = website_full_text.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Take the list of <p> tags and get the nested text as strings
    website_text = []
    for i in range(len(website_raw_text)):
        website_text.append(website_raw_text[i].getText())
#        print(website_text[i])

    # Amazon Polly API Call
    polly = boto3.client("polly")
    audio_response = polly.synthesize_speech(
        Text = "The cake is a lie. The cake is a Lie. Hello Dave, I can't let you do that Dave.",
        TextType = "text",
        OutputFormat = "mp3",
        VoiceId="Joanna"
    )
    
    print(audio_response)
    with closing(audio_response['AudioStream']) as stream:
        with open('audio_file.mp3', 'wb') as audio_file:
            audio_file.write(stream.read())

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
