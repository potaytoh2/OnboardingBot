import requests
from bs4 import BeautifulSoup
import html2text
import json
import os

def extract_text_from_website(url, output_directory):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Initialize the HTML to text converter
            h = html2text.HTML2Text()

            # Remove HTML tags and convert to plain text
            plain_text = h.handle(str(soup))

            # Construct the full output file path
            output_file = os.path.join(output_directory, url.split('//')[1].split('.')[1] + '_web_contents.txt')

            # Write the extracted text to a text file in the sourceDocuments directory
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(plain_text)

            print(f"Text from '{url}' extracted and saved to '{output_file}'")

        else:
            print(f"Failed to fetch the web page '{url}'. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
source_directory = './sourceDocuments/'  # Replace with the actual directory path

with open('./links.json', 'r') as json_file:
    websites = json.load(json_file)
    for website in websites:
        extract_text_from_website(website, source_directory)
