from urllib.parse import urlparse,urlunparse,urlencode
import os
import requests

# cameras={"fhaz","rhaz","mast","chemcam","mahli", "mardi","navcam","pancam","minites"}
def build_url(baseurl, rover, args_dict):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urlparse(baseurl))
    url_parts[2]=url_parts[2]+(rover)+"/photos"

    url_parts[4]=urlencode(args_dict)
    return urlunparse(url_parts)

rovers={"curiosity", "opportunity", "spirit"}

# Get your api_key by registering your details.

api_key="DEMO_KEY"

base_url="https://api.nasa.gov/mars-photos/api/v1/rovers/"


for rover in rovers:
    if rover is "curiosity":
        cameras = {"fhaz", "rhaz", "mast", "chemcam", "mahli", "mardi", "navcam"}
    else:
        cameras = {"fhaz", "rhaz", "navcam", "pancam", "minites"}
    for camera in cameras:
        for sol in range(1,1000):
            for page in range(1,6):
                args = {'sol': sol,'camera':camera,'page':page, 'api_key': api_key}
                url1 = build_url(base_url, rover, args)
                data=requests.get(url1).json()
                for item in data['photos']:
                    r=requests.get(item['img_src'])
                    url_parts=list(urlparse(item['img_src']))
                    file_parts=url_parts[2].rsplit('/',1)

                    directory="./" + rover + "/" + camera + "/"+file_parts[0]
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open(directory+'/'+file_parts[1], 'wb') as f:
                        f.write(r.content)
                        print("Successfully downloaded " +item['img_src'])
