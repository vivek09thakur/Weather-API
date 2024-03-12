import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self) -> None:
        self.url = 'https://www.google.com/search?q='
        pass

    def request_google(self, query):
        try:
            query_url = self.url + query
            response = requests.get(query_url)
            response.raise_for_status()
            self.context = response.content
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during HTTP Request: {str(e)}")
            self.context = None

    def scrape_data(self, query):
        self.request_google(query=query)

        if not self.context:
            return {}

        try:
            self.soup = BeautifulSoup(self.context, 'html.parser')
        except Exception as e:
            print(f"Unable to parse HTML: {str(e)}")
            self.soup = None

        if not self.soup:
            return {}

        temp = self.soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'})
        if not temp:
            return {}
        temp = temp.text

        listdiv = self.soup.find_all('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        if not listdiv:
            return {}

        description = self.soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'})
        if not description:
            return {}
        description = description.text

        data = description.split('\n')
        time, sky = data[0][:-3], data[1]

        return {"temp": temp, "time": time, "sky": sky}


if __name__ == "__main__":
    scraper = Scraper()
    data = scraper.scrape_data("what is the weather of phusro")
    if data:
        print(data)
    else:
        print("No valid data found.")