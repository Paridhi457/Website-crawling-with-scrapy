import pandas as pd
import requests #for making HTTP requests
from bs4 import BeautifulSoup #for parsing HTML
import re #for working with regular expressions 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Load the extracted links from the Excel file
df_links = pd.read_excel('extracted_links.xlsx')

# Create a new DataFrame for the extracted information
df_extracted = pd.DataFrame(columns=['Url', 'Filename', 'Status Code', 'Wordcount'])

# Set up Selenium WebDriver with headless Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)


# Iterate over each link and download the HTML page
total_links = len(df_links)
for i, row in df_links.iterrows():
    url = row['internal_link']
    filename = url.split('/')[-1] + '.html' #taking the last part of the url and adding .html to it 
    filename = re.sub(r'[<>:"/\\|?*]', '', filename) #takes three arguments-patterns to match, replacement string and the input string #replaces all occurrences of the matched pattern in the input string with the replacement string
    try:
        response = requests.get(url) #used to make an HTTP get request to the url
        status_code = response.status_code #obtain status code of the response 

        # Save the HTML page to a file
        #open the file in write mode and write the content of the HTTP response to that file 
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)

        # Extract the text from the HTML page and calculate word count
        # soup object to remove script, style, head, title, meta, and other non-visible elements from the HTML page before extracting the visible text
        soup = BeautifulSoup(response.content, 'html.parser') #parsing the text of the HTTP response
        for element in soup(['script', 'style', 'head', 'title', 'meta', '[document]']):
            element.extract()
        visible_text = soup.get_text() #get_text() method is used to extract the text from the HTML, removing any HTML tags and other markup
        word_count = len(re.findall(r'\w+', visible_text)) #re.findall() function is used with the regular expression (r'\w+') to count the number of words in the extracted text

        # Add the information to the DataFrame
        df_new_row = pd.DataFrame({
            'Url': url,
            'Filename': filename,
            'Status Code': status_code,
            'Wordcount': word_count
        }, index=[0])
        df_extracted = pd.concat([df_extracted, df_new_row], ignore_index=True)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred for URL: {url}")
        df_new_row = pd.DataFrame({
            'Url': url,
            'Filename': filename,
            'Status Code': 'Error',
            'Wordcount': 0
        }, index=[0])
        df_extracted = pd.concat([df_extracted, df_new_row], ignore_index=True)

    # Print progress update
    print(f"Processed link {i+1}/{total_links}")

    # Quit the Selenium WebDriver
    driver.quit()

# Save the extracted information to an Excel file
output_filename = 'extracted_information.xlsx'
df_extracted.to_excel(output_filename, index=False)
print(f"Extraction completed. Output saved to {output_filename}")






