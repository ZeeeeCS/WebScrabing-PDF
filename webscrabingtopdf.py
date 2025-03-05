from bs4 import BeautifulSoup
import requests
import PyPDF2
import io
import concurrent.futures
import os

# Constants
BASE_URL = "https://www.happinessresearchinstitute.com/"
OUTPUT_FOLDER = "extracted_texts"
LOG_FILE = "error_log.txt"

# Ensure output directory exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def fetch_pdf_links(base_url):
    """Fetch PDF links from the website."""
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            full_url = href if href.startswith('http') else base_url + href
            pdf_links.append(full_url)
    return pdf_links

def download_and_extract_text(pdf_url):
    """Download a PDF and extract its text."""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Process PDF
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        extracted_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text() + "\n"

        # Save extracted text
        pdf_name = pdf_url.split("/")[-1].replace(".pdf", ".txt")
        output_path = os.path.join(OUTPUT_FOLDER, pdf_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"Successfully processed: {pdf_url}")
    except Exception as e:
        # Log errors
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(f"Error processing {pdf_url}: {e}\n")
        print(f"Error processing {pdf_url}: {e}")

def main():
    pdf_links = fetch_pdf_links(BASE_URL)
    if not pdf_links:
        print("No PDF links found on the page.")
        return

    print(f"Found {len(pdf_links)} PDF links. Starting download and extraction...")

    # Use multithreading for parallel processing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_and_extract_text, pdf_links)

    print(f"Processing complete. Check the '{OUTPUT_FOLDER}' folder for extracted texts.")
    if os.path.exists(LOG_FILE):
        print(f"Errors were logged in '{LOG_FILE}'.")

if __name__ == "__main__":
    main()
