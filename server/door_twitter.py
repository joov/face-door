import os, yaml
from datetime import datetime
import ext_api as ext_api

def get_api():
    
    if not hasattr(get_api, 'secrets'):
        file = open(os.path.abspath(os.path.join('secrets.yml')), 'r')

        secrets = yaml.load(file)

    print (secrets['Consumer_Key'])
    api = ext_api.ExtApi(consumer_key=secrets['Consumer_Key'],
                      consumer_secret=secrets['Consumer_Secret'],
                      access_token_key=secrets['Access_Token'],
                      access_token_secret=secrets['Access_Token_Secret'])
    return api

def get_other_user():
    if not hasattr(get_other_user, 'name'):
        file = open(os.path.abspath(os.path.join('secrets.yml')), 'r')

        secrets = yaml.load(file)
        name = secrets['Other_User']

    return name
        

def send_message(text, image_path):
    api = get_api()

    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tweet_text = "{0} at {1}".format(text, time_str)
    if image_path is None:
        
        try:
            print('Posting direct message')
            api.PostDirectMessage(
                          text=tweet_text,
                          screen_name=get_other_user())

        except BaseException:
             print("Unexpected error while sending direct message:", sys.exc_info()[0])

    else:
        file = open(image_path, 'rb')
        data = file.read()

        try:
            print('Posting direct message with image')
            media_id = api.UploadMediaSimple(
                          media=data,
                          additional_owners=[get_other_user()],
                          media_category=None)
            api.PostDirectMessageWithImage(
                          texst=tweet_text,
                          media_id=media_id,
                          screen_name=get_other_user())

        except BaseException:
             print("Unexpected error while sending direct message:", sys.exc_info()[0])

    return 'Messge sent!'