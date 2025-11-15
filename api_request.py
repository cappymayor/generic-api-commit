import requests
import access_key

endpoint = f"https://content.guardianapis.com/search?q=Russian/Ukraine&api-key={access_key.api_key}"

r = requests.get(endpoint)
# print(r.json())

data = r.json()

pages = data['response']['pages']

result = data['response']['results']


for article in result:
    charlist = []
    char = { 
        'article' : article['id'],
        'type' : article['type'],
        'section_id' : article['sectionId'],
        'section_name' : article['sectionName']
    }
    charlist.append(char)
    print(charlist)

