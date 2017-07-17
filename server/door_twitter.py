import yaml
from datetime import datetime
from TwitterAPI import TwitterAPI


def get_api():
    
    if not hasattr(get_api, 'secrets'):
        file = open('secrets', 'r')

        secretes = yaml.load_all(file)

    api = TwitterAPI(secrets['Consumer_Key'],
                 secrets['Consumer_Secret'],
                 secrets['Access_Token'],
                 secrets['Access_Token_Secret'])
    return api
        



def send_message(text, image_path):
    secrets = get_secrets

    api = get_api()

    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tweet_text = "{0} at {1} at {}".format(text, time_str)
    if image_path is None:
        r = api.request('statuses/update', {'status': TWEET_TEXT})
    else:
        file = open(image_path, 'rb')
        data = file.read()
        r = api.request('statuses/update_with_media',
                {'status': tweet_text},
                {'media[]': data})

    print('SUCCESS' if r.status_code == 200 else 'FAILURE')




    print('SUCCESS' if r.status_code == 200 else 'FAILURE')
    