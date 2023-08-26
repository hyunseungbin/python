from urllib.request import Request, urlopen
import json
import pprint

def find_list(listdata, key, value):
    for item in listdata:
        if item.get(key) == value:
            return item
    return None


header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "referer" : "https://www.youtube.com"
}

video_url = "vPk2JMHL880"
url = f"https://www.youtube.com/watch?v={video_url}"

watch_html = urlopen(url).read().decode("utf-8")


parse = "ytInitialPlayerResponse = "

start_index = watch_html.find(parse)
end_index = watch_html.find("};", start_index+1) if start_index >= 0 else 0

if start_index < end_index:
    
    h = watch_html[start_index + len(parse):end_index+1]
    json_data = json.loads(h)
    
    aformats = json_data["streamingData"]["adaptiveFormats"]
    data = next((item for item in aformats if item["itag"] == 137), None)
    if data is not None:
        sample_url = data["url"]
        quaulity = data["quality"]
        request = Request(sample_url, headers=header)
        
        r = urlopen(request)
        file_size = r.headers['Content-Length']
        print(r.headers)