from selenium import webdriver
from selenium.webdriver.common.by import By
import time
columns = ["Planet Name", "Parsecs from Earth", "Planet Mass", "Stellar Magnitude", "Discovery Date", "Planet Radius", "Planet Type", "Discovery Method", "Orbital Radius", "Orbital Period", "Eccentricity"]

# URL of the webpage
url = "https://science.nasa.gov/exoplanets/exoplanet-catalog/"
# url = "https://disfold.com/sector/energy/companies/?page=1"

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Give the driver some time to load the page
time.sleep(5)

# Open the webpage
driver.get(url)

# Locate elements with the specified class name
items = driver.find_elements(By.CLASS_NAME, "hds-content-item")

print(items[0].text)

contents = {}
lines = items[0].text.split('\n')
contents["Planet Name"] = lines[0]
for line in lines:
    if ': ' in line:
        key, value = line.split(': ', 1)  # Split into key and value, limit to 1 split
        contents[key] = value 
print(contents)
# Close the driver after use
driver.quit()
