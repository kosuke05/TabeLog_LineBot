import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup

class scraping:
    def __init__(self,company,page,num):
        self.company = company
        self.page = page
        self.num = num
        self.save_text()

    def save_text(self):
        html=requests.get(self.page).text
        soup=BeautifulSoup(html,"html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        text=soup.get_text()
        text = ''.join(text.split())

        with open("C:/Users/shine/OneDrive/prog/Xedge03/output_data/company/"+str(self.num)+".txt", mode="w", encoding='utf-8', errors='ignore') as f:
            f.write(text)

if __name__ == "__main__":
    f = open('C:/Users/shine/OneDrive/prog/Xedge03/input_data/CompanysData.csv', 'r+', encoding='utf-8', errors='ignore')
    rows = csv.reader(f)
    header = next(rows) 

    num = 0
    for row in rows:  
        num = num+1
        scraping(row[1],row[2],num)
        print(row[1],row[2])
    f.close()