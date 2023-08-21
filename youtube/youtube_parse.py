import requests
import json
import pprint
header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "referer" : "https://www.youtube.com"
}
url = "https://www.youtube.com/watch?v=vPk2JMHL880"

parse = "ytInitialPlayerResponse = "

r = requests.get(url=url,headers=header)
start_index = r.text.find(parse)
end_index = r.text.find("};", start_index+1) if start_index >= 0 else 0

if start_index < end_index:
    
    h = r.text[start_index + len(parse):end_index+1]
    json_data = json.loads(h)
    with open("python\youtube\youtube_data.txt","wt",encoding="utf-8") as out:
        pprint.pprint(json_data,stream=out)