#http://docs.python-requests.org/en/latest/user/quickstart/
import json
import requests

print('========================Request example=================================')
r = requests.get('https://api.github.com/events')
print(r)

# #make-a-request
print('=======================Post example==================================')
r = requests.post('http://httpbin.org/post', data = {'key':'value'})
print(r)

print('=======================Params example=================================')
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('http://httpbin.org/get', params=payload)
print(r.url)


print('=======================Json example================================')
r = requests.get('https://api.github.com/events')
print (r.json)


print('=======================Headers example================================')
r = requests.get('http://httpbin.org/get?key2=value2&key1=value1', stream=True)
print(r.headers['Content-Type'])

r.headers.get('content-type')


print('======================Coockies==============================')
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
print(r.cookies)


print('======================Custom Headers==============================')
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)
print(r)

