import requests
import os

CLIENT_FOLDER = 'client'
if not os.path.exists(CLIENT_FOLDER):
    os.makedirs(CLIENT_FOLDER)


def upload_png(filename):
    url = 'http://127.0.0.1:5000/upload_png'
    # files = {'file': open(os.path.join(CLIENT_FOLDER, filename), 'rb')}
    files = {'file': open(filename, 'rb')}
    response = requests.post(url, files=files)
    print(response.text)

#
# def upload_array(filename):
#     url = 'http://127.0.0.1:5000/upload_array'
#     files = {'file': open(os.path.join(CLIENT_FOLDER, filename), 'rb')}
#     response = requests.post(url, files=files)
#     print(response.text)
#
#
# def download_png(filename):
#     url = f'http://127.0.0.1:5000/download_png/{filename}'
#     response = requests.get(url)
#     with open(os.path.join(CLIENT_FOLDER, filename), 'wb') as f:
#         f.write(response.content)
#     print("PNG file downloaded successfully")
#
#
# def download_array(filename):
#     url = f'http://127.0.0.1:5000/download_array/{filename}'
#     response = requests.get(url)
#     with open(os.path.join(CLIENT_FOLDER, filename), 'wb') as f:
#         f.write(response.content)
#     print("NumPy array file downloaded successfully")
#
#
# # if __name__ == '__main__':
#     # upload_png('4_color.png')
#     # download_png('2_color.png')
#     #
#     # upload_array('3_depthData.npy')
#     # download_array('2_depthData.npy')
