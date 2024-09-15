from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import pandas as pd

columns=["World Rank", "National Rank", "Name", "Image Urls", "Affiliations", "Country", "H-index", "Citations","#DBLP"]

def get_scholar_details(row):
    details=row.text.split('\n')
    contents={}
    contents['World Rank']= details[0]
    contents['National Rank']= details[1]
    contents['Name']= details[2]
    contents['Affiliations']= details[3].split(',')[0]
    contents['Country']= details[3].split(',')[1].strip()
    contents['H-index']= details[4]
    contents['Citations']= details[5].replace(',','')
    contents['#DBLP']= details[6].replace(',','')
    contents['Image Urls']= row.find_element(By.CLASS_NAME,'lazyload').get_attribute('src')
    
    return contents
def main():

    scholar_contents=[]
    for page_id in range(1,21):
        webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service)
       
        url = f"https://research.com/scientists-rankings/computer-science?page={page_id}"
        driver.get(url)
       
        rankings=driver.find_element(By.ID, 'rankingItems')
        rows=rankings.find_elements(By.CLASS_NAME, 'cols')
        for idx,row in enumerate(rows):
            if idx%4==0:
                scholar_contents.append(get_scholar_details(row))
        driver.quit()   

    print(len(scholar_contents))
    df=pd.DataFrame(data=scholar_contents,columns=columns)
    df.to_csv('best_cs_scientiest.csv',index=False)

if __name__ == "__main__":
    main()
