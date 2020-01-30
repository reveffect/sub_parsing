import threading
import requests
import time

token = '581aa7cd581aa7cd581aa7cd20587466cf5581a581aa7cd061b93ff083b7050d009f6e0'

version = 5.103
id = '365133336'
count = 100
offset = 0
members=[]

response = requests.get('https://api.vk.com/method/users.getSubscriptions',
                        params={
                            'access_token': token,
                            'v': version,

                            'user_id': id,

                        })
data = response.json()['response']['groups']['items']

data_set = set(data)

while offset < 20000:

    mem=requests.get('https://api.vk.com/method/groups.getMembers',
                        params={
                                "count": 1000,
                                'access_token':token,
                                'v':version,
                                'group_id':'117227746',
                                'offset':offset
                               })

    members.extend(mem.json()["response"]["items"])
    offset=offset+1000

collect_members=[]
active_members=[]


def checking(members,data_set):

    for member in members:

        users=requests.get('https://api.vk.com/method/users.get',
                        params={

                                'access_token':token,
                                'v':version,
                                'user_ids': member



                        })
        try:
            deact=users.json()['response'][0]['deactivated']

        except:
            if users.json()['response'][0]['is_closed'] == False:
                check_members = requests.get('https://api.vk.com/method/users.getSubscriptions',
                                         params={
                                             'access_token': token,
                                             'v': version,

                                             'user_id': member,

                                         })
                mem_data = check_members.json()['response']['groups']['items']
                md = set(mem_data)
                active_members.append(member)
                print("hi")

                if len(data_set.intersection(md)) > 2:
                    collect_members.append(member)





def ping(url):
    res = requests.get(url)
    print(f'{url}: {res.text}')


urls = [
    'http://httpstat.us/200',
    'http://httpstat.us/400',
    'http://httpstat.us/404',
    'http://httpstat.us/408',
    'http://httpstat.us/500',
    'http://httpstat.us/524'
]

start = time.time()
for url in urls:
    ping(url)
print(f'Sequential: {time.time() - start : .2f} seconds')

print()

start = time.time()
threads = []
for url in urls:
    thread = threading.Thread(target=ping, args=(url,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()



for member in members:
    thread =threading.Thread(target=checking, args=(members,data_set))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

print(f'Threading: {time.time() - start : .2f} seconds')
