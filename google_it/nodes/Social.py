class Social:
    """Class representing a social media profile."""

    def __init__(self, name, url, icon):
        """
        Initialize a new Social object.

        Parameters:
        - name (str): The name of the social media platform.
        - url (str): The URL of the social media profile.
        - icon (str): The URL of the icon representing the social media platform.
        """
        self.name = name
        self.url = url
        self.icon = icon
