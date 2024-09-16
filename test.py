from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

columns=["Planet Name","Parsecs from Earth", "Planet Mass", "Stellar Magnitude", "Discovery Date", "Planet Radius", "Planet Type", "Discovery Method", "Planet Mass", "Discovery Date", "Orbital Radius", "Orbital Period", "Eccentricity"]


def get_exoplanet_details(exoplanet):
    webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service)
        
    contents ={}
    lines = exoplanet.text.split('\n')
    contents["Planet Name"] = lines[0]
    for line in lines[1:]:
        key, value = line.split(': ', 1)  # Split into key and value, limit to 1 split
        contents[key] = value  
    url2_plants = f"https://science.nasa.gov/exoplanet-catalog/{contents["Planet Name"]}/"
    driver.get(url2_plants)
    planet_info_blocks = driver.find_elements(By.CLASS_NAME, "smd-acf-grid-col")
    for block in planet_info_blocks:
        label = block.find_element(By.CLASS_NAME, "text-bold").text.strip(": ")  # Label text, like "Planet Radius"
        value = block.find_element(By.TAG_NAME, "span").text.strip()  # The value, like "1.026 x Jupiter"
        label.replace(':',"")
        contents[label] = value
    driver.quit()
    return contents

def main():
    exoplanet_content =[]
    for page_id in range(1, 384):
        webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
        service = Service(webdriver_path)
        driver = webdriver.Chrome(service=service)
        url= f"https://science.nasa.gov/exoplanets/exoplanet-catalog/?pageno={page_id}&content_list=true"
        driver.get(url)
        exoplanets = driver.find_elements(By.CLASS_NAME, "hds-content-item")
        driver.quit()
        for exoplanet in exoplanets:
            exoplanet_content.append(get_exoplanet_details(exoplanet))
    
    df=pd.DataFrame(data=exoplanet_content,columns=columns)
    df.to_csv('nasa_exoplanets.csv',index=False)  


if __name__ == "__main__":
    main()
