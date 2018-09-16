import json
import requests
import bs4
import boto3
from contextlib import closing

def web_scraper(event, context):
    
    # Grab the url from the event json and grab the source file using requests
    url = event['url_search']
    response = requests.get(url)

    # convert the source html to a beautifulSoup object, select all <p> tags
    website_full_text = bs4.BeautifulSoup(response.text, features="lxml")
    # website_raw_text = website_full_text.select('p')
    website_raw_text = website_full_text.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Take the list of paragraphs and headers and get the nested text as strings
    website_text = []
    for i in range(len(website_raw_text)):
        website_text.append(website_raw_text[i].getText())
    
    # Concatinate all pieces of text in website_text into a single string
    # This will be used for the Long Audio File
    full_text = ''
    for i in website_text:
        full_text += i

    # Amazon Polly API Call
#    polly = boto3.client("polly")
#    audio_response = polly.synthesize_speech(
#        Text = "The cake is a lie. I'm sorry Dave, I'm afraid I can't do that.",
#        TextType = "text",
#        OutputFormat = "mp3",
#        VoiceId="Joanna"
#    )
    
    # Send mp3 to audio file    
#    with closing(audio_response['AudioStream']) as stream:
#        with open('audio_file.mp3', 'wb') as audio_file:
#            audio_file.write(stream.read())
    
    # Testing to see if a Long Audio File would be better
    bucket_name = event['bucket_name']
    long_audio = polly.start_speech_synthesis_task(
        OutputFormat = 'mp3',
        OutputS3BucketName = bucket_name,
        VoiceId = "Joanna",
        Text = full_text,
        TextType = 'text'
    )

    return event
