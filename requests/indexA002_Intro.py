"""
Lien : https://www.youtube.com/watch?v=zZU0JZmIvKA&list=PLJ1odve0o6dX5ndJ5lwiCOR58ycB1rcrV&index=4
Cours : Python Requests | JSON

Date : 16-12-23
"""

import requests

data = {'firsName': 'John'}

r = requests.get("https://api.github.com/events")
events = r.json()
print(events[0]['id'])
