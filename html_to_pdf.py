import pdfkit
import requests


def download_html(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)


def convert_html_to_pdf(html_path, pdf_path):
    pdfkit.from_file(html_path, pdf_path)


# URL of the HTML page to download
# html_url = "http://example.com/path/to/html_file.html"

# Path to save the downloaded HTML file
html_filename = "report.html"
html_path = html_filename

# Path to save the generated PDF file
pdf_filename = "generated_pdf.pdf"
pdf_path = pdf_filename

# Download the HTML file
# download_html(html_url, html_path)

# Convert HTML to PDF
convert_html_to_pdf(html_path, pdf_path)

print(f"HTML file downloaded: {html_path}")
print(f"PDF file generated: {pdf_path}")
