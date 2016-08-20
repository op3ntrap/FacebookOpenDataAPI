import urllib
import threading
import random

def random_file_name():
    t = random.random()*100000000000
    return str(int(t)) + ".pdf"

for a in range(1,5):
    print random_file_name()

def download_upload_delete(link):
    file_name = random_file_name()
    urllib.urlretrieve (link)


def get_downloadurls(csv_file):
    i = 2
    filepath = "jmlr_disdr.xlsx"
    from openpyxl import load_workbook
    url = "<Url>"
    while (url != None):
        url = load_workbook (filepath).get_sheet_by_name ("Sheet1").cell (row=i, column=1).value
        threading.Thread (target=download_upload_delete, args=(url,))
        i += 1