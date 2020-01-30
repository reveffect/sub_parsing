import requests
import time

token = '581aa7cd581aa7cd581aa7cd20587466cf5581a581aa7cd061b93ff083b7050d009f6e0'

version = 5.103
id= '365133336'
count = 100
offset = 0
all_posts = []

response = requests.get('https://api.vk.com/method/users.getSubscriptions',
                            params={
                                'access_token':token,
                                'v':version,
        
                                'user_id': id,

                            })
data = response.json()['response']['groups']['items']


data_set=set(data)
a=[]


'''for i in range(len(data)):
    q=requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'access_token':token,
                                'v':version,

                                'group_ids':data[i]

                            })
    a.extend(q)
'''

'''for dat in data :
    
    q = requests.get('https://api.vk.com/method/groups.getById',
                 params={
                     'access_token': token,
                     'v': version,

                     'group_ids': dat

                 })
aq=q.json()'''





members=[]
start_time = time.time()
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


'''collect_members=[]
mem_data=[]
for member in members:
    users = requests.get('https://api.vk.com/method/users.get',
                         params={

                             'access_token': token,
                             'v': version,
                             'user_ids': member

                         })
    user = users.json()

        check_members= requests.get('https://api.vk.com/method/users.getSubscriptions',
                        params={
                            'access_token': token,
                            'v': version,

                            'user_id': member,

                        })

        mem_data = check_members.json()['response']['groups']['items']
        md=set(mem_data)
        if len(data_set.intersection(md))>1:
            collect_members.append(member)'''



collect_members=[]
active_members=[]
for member in members:

    users=requests.get('https://api.vk.com/method/users.get',
                        params={

                                'access_token':token,
                                'v':version,
                                'user_ids': member



                        })
    try:
        deact=users.json()['response'][0]['deactivated']
        print(deact)
        print(member)

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






with open("файл.txt", "w") as file:
    for item in collect_members:
        print(item, file=file)

print(len(active_members))
print("--- %s seconds ---" % (time.time() - start_time))



