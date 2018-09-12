import json
import requests
import bs4
import selenium


def web_scraper(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }
    
    # Grab the url from the event json and grab the source file using requests
    url = event['url_search']
    response = requests.get(url)

    # convert the source html to a beautifulSoup object, select all <p> tags
    website_full_text = bs4.BeautifulSoup(response.text)
    website_raw_text = website_full_text.select('p')

    # Take the list of <p> tags and get the nested text as strings
    website_text = []
    for i in range(len(website_raw_text)):
        website_text.append(website_raw_text[i].getText())


    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
