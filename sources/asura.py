from utils.session import SESSION

from .base import Chapter, Series, Source


class AsuraChapter(Chapter):
    def name(self):
        res = SESSION.get(self.url)
        data = res.json()
        s_title = data["data"]["series"]["title"]
        ch_title = data["data"]["chapter"]["title"]
        ch_number = data["data"]["chapter"]["number"]
        
        return (s_title, f"Ch {ch_number:03} - {ch_title}")
    
    def get_pages(self):
        res = SESSION.get(self.url)
        print(res.text)
        print(self.url)
        data = res.json()
        # data = get(self.url)
        pages = data["data"]["chapter"]["pages"]
        return tuple(page["url"] for page in pages)
    
class AsuraSeries(Series):
    def get_chapters(self):
        res = SESSION.get(f"{self.url}/chapters")
        data = res.json()
        # data = get(f"{self.url}/chapters")
        chapters = data["data"]
        return tuple(AsuraChapter(f"{self.url}/chapters/{chapter["number"]}") for chapter in chapters)

class Asura(Source):
    url = "https://api.asurascans.com/api/series"
    
    def search_series(cls, query):
        res = SESSION.get(f"{cls.url}", params={"search": query})
        data = res.json()
        # data = get(f"{cls.url}", params={"search": query})
        # pprint(data)
        series_l = data["data"]
        return tuple(AsuraSeries(f"{cls.url}/{series["slug"]}") for series in series_l)

    def get_series(cls, slug):
        return AsuraSeries(f"{cls.url}/{slug}")
