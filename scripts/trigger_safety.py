#this is just a file to trigger a safety scan

import urllib3

http = urllib3.PoolManager()
response = http.request('GET', 'https://httpbin.org/ip')
print(response.data)