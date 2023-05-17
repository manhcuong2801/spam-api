import threading
import requests
import asyncio
import aiohttp

# Login

url_login = 'http://10.1.10.36:8002/api/v1/users/login/'

body = {
    "login_id": "1090149601",
    "password": "a1234567",
    "device_type": "FrontWeb",
    "wl_code": "10"
}

response_login = requests.post(url=url_login, data=body)
token = response_login.json().get('data').get('access_token')

print(f'Access Token: {token}')

# Get User Information

url_account_infor = 'http://10.1.10.36:8002/api/v1/mt5/mt5_infor/?account_id=1090149601'


async def get_response(session, url):
    try:
        headers = {
            'Authorization': f'Bearer {token}'
        }
        async with session.get(url=url, headers=headers) as response:
            return response.json()
    except Exception as err:
        print(f'Loi cmnr: {err}')


# Define a function to make multiple API requests to a single endpoint
async def make_multiple_requests(url, num_requests):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Make the first request to establish the connection
            await response.text()
            # Reuse the same connection for subsequent requests
            tasks = []
            for _ in range(num_requests - 1):
                tasks.append(session.get(url=url, headers=headers))
            responses = await asyncio.gather(*tasks)
            # Process the responses as needed
            for response in responses:
                # Process each response
                await response.text()

# Run the event loop
loop = asyncio.get_event_loop()
url = url_account_infor
num_requests = 100 

loop.run_until_complete(make_multiple_requests(url, num_requests))

# def get_response():
#     try:
#         headers = {
#             'Authorization': f'Bearer {token}'
#         }
#         response_list_acc = requests.get(url=url_account_infor, headers=headers)
#         print(response_list_acc)
#     except Exception as err:
#         print(f'Loi cmnr: {err}')


# threads = []
# a = 0
# for e in range(25):
#     for i in range(5):
#         x = threading.Thread(target=get_response())
#         x1 = threading.Thread(target=get_response())
#         x2 = threading.Thread(target=get_response())
#         x3 = threading.Thread(target=get_response())
#         x4 = threading.Thread(target=get_response())
#         x5 = threading.Thread(target=get_response())
#
#         threads.append(x)
#         threads.append(x1)
#         threads.append(x2)
#         threads.append(x3)
#         threads.append(x4)
#         threads.append(x5)
#         x.start()
#         x1.start()
#         x2.start()
#         x3.start()
#         x4.start()
#         x5.start()
#
#     for thread in threads:
#         thread.join()
#         print(f'Running threads {thread.name}')

print('DONE')

