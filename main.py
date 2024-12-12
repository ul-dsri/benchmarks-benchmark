import csv
import os
import requests

from datetime import datetime

def define_env(env):
    @env.macro
    def list_pdfs(pdf_dir='pdf'):
        pdf_path = os.path.join('./docs', pdf_dir)
        pdf_full_path = os.path.abspath(pdf_path)
        pdf_files = [f for f in os.listdir(pdf_full_path) if f.endswith('.pdf')]
        pdf_files.sort()

        markdown_links = ""
        for pdf in pdf_files:
            pdf_link = f"{pdf_dir}/{pdf}"
            markdown_links += f"- [{pdf}]({pdf_link})\n"
        return markdown_links


    @env.macro
    def get_latest_pdf_anchor(pdf_dir='pdf'):
        pdf_path = os.path.join('./docs', pdf_dir)
        pdf_full_path = os.path.abspath(pdf_path)
        pdf_files = [f for f in os.listdir(pdf_full_path) if f.endswith('.pdf') and "_normalized.pdf" not in f]

        if not pdf_files:
            return None  # Return None if no PDF files are found

        # Get the full path for sorting by creation time
        pdf_files_full_path = [os.path.join(pdf_full_path, f) for f in pdf_files]
        newest_pdf = max(pdf_files_full_path, key=os.path.getctime)  # Sort by creation time

        # Return the newest PDF in the desired format
        newest_pdf_name = os.path.basename(newest_pdf)
        newest_pdf_link = f"{pdf_dir}/{newest_pdf_name}"
        return f"- [Latest paper version]({newest_pdf_link})\n"


    @env.macro
    def get_latest_pdf_url(pdf_dir='pdf'):
        pdf_path = os.path.join('./docs', pdf_dir)
        pdf_full_path = os.path.abspath(pdf_path)
        pdf_files = [f for f in os.listdir(pdf_full_path) if f.endswith('.pdf') and "_normalized.pdf" not in f]

        if not pdf_files:
            return None  # Return None if no PDF files are found

        # Get the full path for sorting by creation time
        pdf_files_full_path = [os.path.join(pdf_full_path, f) for f in pdf_files]
        newest_pdf = max(pdf_files_full_path, key=os.path.getctime)  # Sort by creation time

        # Return the newest PDF in the desired format
        newest_pdf_name = os.path.basename(newest_pdf)
        newest_pdf_link = f"{pdf_dir}/{newest_pdf_name}"
        return newest_pdf_link


    @env.macro
    def get_questionnaire_list_from_s3(csv_url="https://dl.dsri.org/papers/benchmarks-benchmark/questionnaire.csv"):
        return get_pdf_list_from_s3(csv_url)


    @env.macro
    def get_pdf_list_from_s3(csv_url="https://dl.dsri.org/papers/benchmarks-benchmark/index.csv"):

        response = requests.get(csv_url)
        response.raise_for_status()  # Raise an error if the request fails

        # Decode the CSV content
        content = response.text
        markdown_list = []

        # Parse the CSV content
        reader = csv.reader(content.splitlines())

        # Skip header in CSV content
        next(reader)

        for row in reader:
            if len(row) != 2:
                continue  # Skip rows that don't have exactly two columns
            filename, file_url = row
            markdown_list.append(f"- [{filename}]({file_url})")

        return "\n".join(markdown_list)


    @env.macro
    def read_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()


    @env.macro
    def current_date():
        return datetime.now().strftime('%Y-%m-%d')

