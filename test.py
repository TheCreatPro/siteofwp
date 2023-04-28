from requests import post, get


print(get('http://localhost:5000/lastnews').json())
