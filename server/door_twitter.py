import sys, os, yaml, traceback
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
                          user_id=get_other_user())

        except BaseException:
             print("Unexpected error while sending direct message")
             traceback.print_exc(file=sys.stdout)

    else:

        try:
            print('Posting direct message with image {}'.format(image_path))
            media_id = api.UploadMediaSimple(
                          media=image_path)
                          additional_owners=[int(get_other_user())])

            print('Got media id {}'.format(media_id))

            api.PostDirectMessageWithImage(
                          text=tweet_text,
                          media_id=media_id,
                          user_id=get_other_user())

        except BaseException:
             print("Unexpected error while sending direct message")
             traceback.print_exc(file=sys.stdout)

    print('Messge sent!')