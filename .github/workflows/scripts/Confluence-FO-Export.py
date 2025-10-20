import os
import sys
from atlassian import Confluence
from pypdf import PdfMerger

confluence = Confluence(url="https://topicus.atlassian.net", username="npa.screening@topicus.nl", password=sys.argv[1], cloud=True)
pdf_number = 100000

def export_pages(page_ids):
    for page_id in page_ids:
        global pdf_number
        pdf_number+=1
        export_single_page(page_id, pdf_number) 
        
def export_single_page(page_id, name):
    try:
        content = confluence.export_page(page_id)
        with open(str(name) + ".pdf", "wb") as pdf_file:
            pdf_file.write(content)
            pdf_file.close()
            print("Completed")
    except:
        print(f"Exporting page with id {page_id} failed")

def merge_exported_pages():
    merger = PdfMerger()
    pdfs = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.pdf')]
    for pdf in pdfs:
        merger.append(pdf)
    merger.write("FO_en_TO_ScreenIT.pdf")
    merger.close()
    for pdf in pdfs:
        os.remove(pdf)
    print("Export Done")


if __name__ == "__main__":
    if(sys.argv[2] == "volledig"):
# ID FO main page: 715333870
# ID TO main page: 715334845
        export_pages(confluence.get_subtree_of_content_ids(715333870))
        export_pages(confluence.get_subtree_of_content_ids(715334845))
        merge_exported_pages()
    elif(sys.argv[2] == "services"):
# ID Services main page: 637765899
        export_single_page(637765899, "Services")




