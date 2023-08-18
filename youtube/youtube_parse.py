import requests

header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "referer" : "https://www.youtube.com"
}
url = "https://www.youtube.com/watch?v=vPk2JMHL880"

parse = "ytInitialPlayerResponse = "

r = requests.get(url=url,headers=header)
print(r.text)

