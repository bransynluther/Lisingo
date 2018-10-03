import requests
import json
import boto3
import bs4
from contextlib import closing

def web_scraper(event, context):

    # For Debugging the state machine
    print(event)

    # Grab the url from the event json and grab the source file using requests
    url = event['url_search']
    check = url.find("https://")
    if check == -1:
        appended_url = "https://" + url
        response = requests.get(appended_url)
    else:
        response = requests.get(url)

    # convert the source html to a beautifulSoup object, select all <p> tags
    website_full_text = bs4.BeautifulSoup(response.text, features="html.parser")
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
    polly = boto3.client("polly")
    # Testing to see if a Long Audio File would be better
    bucket_name = event['bucket_name']
    voice = event['voice']
    long_audio = polly.start_speech_synthesis_task(
        OutputFormat = 'mp3',
        OutputS3BucketName = bucket_name,
        VoiceId = voice,
        Text = full_text,
        TextType = 'text'
    )

    audio_response_uri = long_audio['SynthesisTask']['OutputUri']
    audio_split = audio_response_uri.split('.')
    audio_split.remove(audio_split[1])
    audio_link = ""
    for i in range(len(audio_split)):
        audio_link += audio_split[i]
        if i < len(audio_split)-1:
            audio_link += '.'
    event['audio_link'] = audio_link
    s3 = boto3.resource("s3")
    objectt = s3.Bucket(bucket_name)
    objectt.Acl().put(ACL='public-read')
    return event

