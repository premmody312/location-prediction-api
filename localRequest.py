import requests
import json
import html2text


url = 'http://localhost:5000/getCoordinates'
myobj = {"Redmi Note X":1.6381444708152757,"Redmi Note X2":1.792622696531886,"Redmi Note X3":1.938144471,"tata":2.5381444708152756,"nilam@japs":2.5381444708152756}

x = requests.post(url, data = json.dumps(myobj))

print(html2text.html2text(x.text))
