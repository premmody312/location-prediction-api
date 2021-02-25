import requests
import json
import html2text


#url = 'https://location-classification-api.herokuapp.com/getCoordinates'
url = 'http://localhost:5000/getCoordinates'
#myobj = {"Redmi Note X":1.6381444708152757,"Redmi Note X2":1.792622696531886,"Redmi Note X3":1.938144471,"tata":2.5381444708152756,"nilam@japs":2.5381444708152756}
#myobj = {"SOMAIYA-WIFI":2.365709966975696,"SOMAIYA-GUEST":2.465709966975696,"Efarm Test":2.207329496997738,"Redmi Note X2":1.6837119514047025,"PARAM2":1.834594843519919,"Lol 5":1.5606702402547667,"Param":2.136366030648211,"Isha":2.2854795341536223,"SemHAll":2.4926226965318863,"email_json":12345};
myobj = {"Efarm Test":0.9106702402547668,"SOMAIYA-WIFI":2.6837119514047023,"SOMAIYA-GUEST":2.6837119514047023,"SemHAll":1.7106702402547669,"ASUS_X00PD":1.4881444708152756,"Isha":1.636366030648211,"Param":1.8381444708152757,"Redmi Note X2":1.8337119514047024,"Lol 2.4":2.2372543403911367,"Lol 5":2.0606702402547667,"Pranav":2.4917233495923496,"Alum Rock":2.736366030648211,"email_json":12223}
x = requests.post(url, json = json.dumps(myobj))

print(html2text.html2text(x.text))
