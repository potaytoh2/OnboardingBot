import requests
from bs4 import BeautifulSoup
import html2text

def extract_text_from_website(url, output_file):
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

            # Write the extracted text to a text file
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write(plain_text)

            print(f"Text from '{url}' extracted and saved to '{output_file}'")

        else:
            print(f"Failed to fetch the web page '{url}'. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage:
website_url = "https://www.healthserve.org.sg/"
output_file = "healthserve_web_contents.txt"
extract_text_from_website(website_url, output_file)
