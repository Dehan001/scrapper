from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

columns = ["Planet Name", "Parsecs From Earth", "Planet Mass", "Stellar Magnitude", "Discovery Date", "Planet Radius", "Planet Type", "Discovery Method", "Orbital Radius", "Orbital Period", "Eccentricity"]

def get_exoplanet_details(exoplanet):
    lines = exoplanet.text.split('\n')
    contents["Planet Name"] = lines[0]
    for line in lines:
        if ': ' in line:
            key, value = line.split(': ', 1)  # Split into key and value, limit to 1 split
            contents[key.strip()] = value.strip()

    webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service)
    contents = {}

    
    try:
        try: 
            url2_planets = f"https://science.nasa.gov/exoplanet-catalog/{contents.get('Planet Name', '').replace(' ', '-').replace('.', '').lower()}/"
            driver.get(url2_planets)
        except:
            url2_planets = f"https://science.nasa.gov/exoplanet-catalog/{contents.get('Planet Name', '').replace(' ', '-').replace('.', '-').lower()}/"
            driver.get(url2_planets)
            
        planet_info_blocks = driver.find_elements(By.CLASS_NAME, "smd-acf-grid-col")

        for block in planet_info_blocks:
            label_element = block.find_element(By.CLASS_NAME, "text-bold")
            value_element = block.find_element(By.TAG_NAME, "span")
            label = label_element.text.strip(": ").replace(':', "").strip()
            value = value_element.text.strip()
            contents[label] = value
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    return contents

def main():
    exoplanet_content = []
    webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
    service = Service(webdriver_path)
    count = 20
    for page_id in range(191, 361):
        driver = webdriver.Chrome(service=service)
        url = f"https://science.nasa.gov/exoplanets/exoplanet-catalog/?pageno={page_id}&content_list=true"
        driver.get(url)
        
        try:
            exoplanets = driver.find_elements(By.CLASS_NAME, "hds-content-item")

            for exoplanet in exoplanets:
                exoplanet_content.append(get_exoplanet_details(exoplanet))

        except Exception as e:
            print(f"An error occurred on page {page_id}: {e}")
        finally:
            driver.quit()
        if (page_id%10==0 or page_id==384):
            print(len(exoplanet_content))
            df = pd.DataFrame(data=exoplanet_content, columns=columns)
            df.to_csv(f'nasa_exoplanets_part{count}.csv', index=False)
            exoplanet_content=[]
            count += 1


if __name__ == "__main__":
    main()
