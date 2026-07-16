import PyPDF2


def get_pdf_page_count(file_path: str):
    try:
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            return num_pages
    except FileNotFoundError:
        print("File not found")
        return 0
    except Exception as e:
        print(e)
        return 0