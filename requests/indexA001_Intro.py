"""
Lien : https://www.youtube.com/watch?v=qriL9Qe8pJc&list=PLJ1odve0o6dX5ndJ5lwiCOR58ycB1rcrV&index=2
Cours : Python Requests | Get and Post Requests

Date : 16-12-2023
"""
import requests

payload = {"firstName":"John", "lastName": "Smith"}

# get : obtention des données
r = requests.get("https://httpbin.org/get", params=payload)
# print(r.url) # URL
# print(r.statuts) # code statuet
# print(r.content) # contenu
# print(r.text) # données sous la forme d'un dictionnaire (format JSON)

# post : MAJ des données
r = requests.post("https://httpbin.org/post", data=payload)
# print(r.text)
