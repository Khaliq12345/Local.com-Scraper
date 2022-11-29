import requests
from bs4 import BeautifulSoup
import pandas as pd
from latest_user_agents import get_random_user_agent
ua = get_random_user_agent()

def scrape():
    item_list = []
    n = 1
    isNext = True
    while isNext:
        print(f'Page {n}')
        headers = {
            'User-Agent': ua
        }
        response = requests.get(f'https://www.local.com/business/results/listing.cfm?s=Restaurant&ar=Miami,Florida&gsp=bDZ2b0RSN1BXUXRacm93VDNMbDZaY3JtaHFZVEdjQWtZNDRnSjdTNFdsMGd5U0VoaG1WdkYybktUQWtuUHA5dzVLUDdaSEVmd3FyYWw0WnNPcHlLT0daQnpGZ0pTTXhEckthM0d1bERBQzJVUFc1KzBkQXhHMTJ4L0JHNHh6UmhocHJSNDVXRGZnR09sNlhGYkt6VVFjc1JiYnYzZEJSM1A5N0Q1ZUp5SEZVZ0FJNk40MHdqUUJEY0FyaDEwZ0RBQ1dlQ2djVWFjSi9IY212aU04N1hIUUR6eVhHUmw2QU9sRDEvUlBhQkE3Y1kxN0g0S1FGRlZOMHpXQS9qMGdCdGEzRTZadkM3Z3lFNnNOWHhmcG00Vk1jT1RVdDNndHZha0hUeUtRbGtXU1dSaEE5aHlhcENIYmtZaktzN0NTZ1c1V1l6MWkwczB1U1pKR3A0WHl0WmVWbno4dmJXTitaU2lMT0xIWWVvdUwyQmdiSzRjY2xHSUwxa0dSbHl0eHZtbGZMV3hsOExwcTVHMDdMWnZuUHVFK2Rhc1hicU43ZWFHS3ViZ09XNUJRbjJoOGE1VnJwb3NxVFNnKzNFRS80dEwrMWhuSDlBQzlreURvQzQxOUVRWW92eGp0ZDMxbE15K2kxZWF1ZW9wQklkUS9hN3ZjR0xTM1puWlVEUmQ3OXd5aHRLa1hrbkNzVStzNFZ4KzVsR0hlZlhtZEUxK3VjbUdzRDdMK1Y4NjkwPQ%3D%3D&_opnslfp=1&lwfilter=&wsrt=&wpn={n}', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            cards = soup.select('.webadLI')
            for card in cards:
                try:
                    name = card.select_one('.webadTitle a').text.strip()
                except:
                    name = None
                try:
                    profile = card.select_one('.webadTitle a')['href'].strip()
                except:
                    profile = None
                try:
                    address = card.select_one('.webadAddress').text.strip()
                except:
                    address = None
                try:
                    phone = card.select_one('.phNum').text.strip()
                except:
                    phone = None
                
                items = {
                    'Name': name,
                    'Profile': profile,
                    'Address': address,
                    'Phone': phone
                }
                item_list.append(items)

            if soup.select_one('.nextBtn.results-spriteimage'):
                next_page = soup.select_one('.nextBtn.results-spriteimage')
                n = n + 1
            else:
                isNext = False
                break
        except:
            break
    df = pd.DataFrame(item_list)
    print(df)
    df.to_csv('local-data.csv')

scrape()
    