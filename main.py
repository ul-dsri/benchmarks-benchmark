import os

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
    def read_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
