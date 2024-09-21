from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

columns = ["Planet Name", "Parsecs from Earth", "Planet Mass", "Stellar Magnitude", "Discovery Date", "Planet Radius", "Planet Type", "Discovery Method", "Orbital Radius", "Orbital Period", "Eccentricity"]



def main():
    exoplanet_content = []
    webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service)
    for page_id in range(70, 261):
        
        url = f"https://science.nasa.gov/exoplanets/exoplanet-catalog/?pageno={page_id}&content_list=true"
        driver.get(url)
        
        try:
            exoplanets = driver.find_elements(By.CLASS_NAME, "hds-content-item")

            for exoplanet in exoplanets:
                contents = {}
                lines = exoplanet.text.split('\n')
                _,contents["Parsecs from Earth"] = lines[1].split(': ', 1)
                contents["Planet Name"] = lines[0]
                for line in lines:
                    if ': ' in line:
                        key, value = line.split(': ', 1)  # Split into key and value, limit to 1 split
                        contents[key.strip()] = value.strip()

                exoplanet_content.append(contents)

        except Exception as e:
            print(f"An error occurred on page {page_id}: {e}")
        
    driver.quit()   
    df = pd.DataFrame(data=exoplanet_content, columns=columns)
    df.to_csv(f'nasa_exoplanets_extra.csv', index=False)    

if __name__ == "__main__":
    main()
