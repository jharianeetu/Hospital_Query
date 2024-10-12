import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of working hospital URLs
hospital_urls = [
    'https://www.mayoclinic.org/',
    'https://my.clevelandclinic.org/',
    'https://www.hopkinsmedicine.org/',
    'https://www.massgeneral.org/',
    'https://www.mountsinai.org/',  # Mount Sinai Health System
    'https://www.charlesriversar.com/',  # Charles River Medical Associates
    'https://www.kp.org/',  # Kaiser Permanente
    'https://www.uwmedicine.org/',  # UW Medicine
    'https://www.caremount.com/',  # CareMount Medical
    'https://www.froedtert.com/',  # Froedtert Health
    'https://www.houstonmethodist.org/',  # Houston Methodist
    'https://www.virginia.edu/health/health-systems/hospital',  # University of Virginia Health System
    'https://www.pennmedicine.org/',  # Penn Medicine
    'https://www.sutterhealth.org/',  # Sutter Health
    'https://www.lifespan.org/',  # Lifespan Health System
    'https://www.hartfordhealthcare.org/',  # Hartford HealthCare
    'https://www.rush.edu/',  # Rush University Medical Center
    'https://www.mercy.com/',  # Mercy Health
    'https://www.stanfordhealthcare.org/',  # Stanford Health Care
    'https://www.ahmchealth.org/',  # AdventHealth
    'https://www.bcm.edu/locations',  # Baylor College of Medicine
]

# Function to scrape hospital data
def scrape_hospital_data(url):
    try:
        response = requests.get(url)
        print(f"Scraping {url} - Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"Failed to retrieve {url}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract hospital name from <title> tag
        name = soup.find('title').text if soup.find('title') else 'Name not found'

        # Since addresses/specialties aren't available directly from the homepage, placeholder text is used
        address = 'Address information not available'
        specialties = 'Specialties information not available'

        print(f"Scraped: {name}, {address}, {specialties}")
        return {'Name': name, 'Address': address, 'Specialties': specialties}
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# List to hold data
hospital_data = []

# Loop through all URLs
for url in hospital_urls:
    data = scrape_hospital_data(url)
    if data:
        hospital_data.append(data)

# Save to CSV if data exists
if hospital_data:
    df = pd.DataFrame(hospital_data)
    df.to_csv('hospitals.csv', index=False)
    print("Data saved successfully.")
else:
    print("No data scraped.")
