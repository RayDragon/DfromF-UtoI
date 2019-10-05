
fb_graph = {
    'PAGE_ACCESS_TOKEN':'EAAd7LhqqdcEBAINg3wqWZCJQRbYYL4ol3bBM5oB0QOnQN9mzjF8IF7jLVJHlYuxx8DTdyQOxxbFtqShHhGZCjQnlAt2ttjVuFmhTdFQEWHzbiCllNsaudX7lWCzhqgQmud08PcOqnoM7ZA6UuVDmXoIpE2X7rQjaa102IlpLgZDZD',
    #'PAGE_ACCESS_TOKEN':'EAALKV1jcWmgBABmsZB18UZBnYdnaCWTlQA8XGril9NeSpHnomeOG8v3P1fCAfPRZA1f1sCxnNXkx6EQOiNrnObQpNBohfi94XrFjkzH81jJEuHhZBfZAZA6B2PHJjdhhNFh7M1D8KsJgbtQMhqcALvZChV9k5f0M1ZCIYCdWH02QOOXhQT7eBua6sr90LHDo45PqcTEbID0uLAZDZD',
    'PAGE_ID':'104045294334792',
    #'PAGE_ID':'702734889928344',

    'SAVE_TO_FOLDER':'images',
    'FILE_TYPES':{'image/jpeg':'jpg', 'image/png':'png'},
    'INSTA_USERNAME':'',
    'INSTA_PASSWORD':''
}
url = 'https://graph.facebook.com/'+fb_graph['PAGE_ID']+'/posts?fields=full_picture&transport=cors&access_token='+fb_graph['PAGE_ACCESS_TOKEN']


import requests, json, os, time, sys


from instapy_cli import client
def upload_files_to_insta(files=[]):
    if len(files) == None:
        return
    else:
        with client(fb_graph['INSTA_USERNAME'], fb_graph['INSTA_PASSWORD']) as cli:
            for file in files:
                cli.upload(file, '')

while True:
    x = requests.get(url)
    # print(x.text)
    try:
        req = json.loads(x.text)
        data_list = req['data']
        files_found=True
        for data in data_list:
            file_list = [x.split('.')[0] for x in os.listdir(fb_graph['SAVE_TO_FOLDER'])]
            n_files = []
            if not data['id'] in file_list:
                print("Downloading File with id", data['id'])
                img = requests.get(data['full_picture'])
                type = fb_graph['FILE_TYPES'][img.headers['Content-Type']]
                file = open(fb_graph['SAVE_TO_FOLDER']+'/'+data['id']+'.'+type, 'wb')
                n_files.append(fb_graph['SAVE_TO_FOLDER']+'/'+data['id']+'.'+type)
                for chunk in img:
                    file.write(chunk)
                file.close()
            else:
                files_found=False
            upload_files_to_insta(n_files)
        if not files_found: 
            print(".", end='')
            sys.stdout.flush()

                
    except Exception as e:
        print("Some error occurred:", req['error']['message'], '\n\n')
        print(str(e), req)
        break
    time.sleep(60) # time to wait in seconds max per hour = 200, so let the min be 18 sec
