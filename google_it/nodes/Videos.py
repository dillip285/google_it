from google_it.utils import Constants


class Video:
    """Class for representing a video."""

    def __init__(self, data):
        """
        Initialize a Video object.

        Parameters:
        - data: Dictionary containing video data.
        """
        self.id = data["id"]
        self.url = data["url"]
        self.title = data["title"]
        self.author = data["author"]
        self.duration = data["duration"]


class Videos:
    @staticmethod
    def parse(soup):
        """
        Parse the videos from the HTML content.

        Parameters:
        - soup: BeautifulSoup object representing the HTML content.

        Returns:
        - List of Video objects.
        """
        videos = []

        data = soup.select(Constants.SELECTORS['VIDEOS'])

        for elem in data:
            anchor_tag = elem.find('a')
            id = anchor_tag.get('href').split('v=')[1] if anchor_tag else None
            url = anchor_tag.get('href') if anchor_tag else None
            title = elem.select_one('a > div > div').get_text().strip() if elem else None
            author = elem.select_one('a > div > div > span').find_next_sibling().find_next_sibling().get_text().replace(
                '·', '').strip() if elem else None
            duration = elem.select_one('div[role="presentation"]').get_text() if elem else None

            if id and url and title and author and duration:
                videos.append(Video({"id": id, "url": url, "title": title, "author": author, "duration": duration}))

        return videos
