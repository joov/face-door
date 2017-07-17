import yaml
from datetime import datetime
import ext_api

def get_api():
    
    if not hasattr(get_api, 'secrets'):
        file = open('secrets', 'r')

        secrets = yaml.load_all(file)

    api = twitter.Api(consumer_key=secrets['Consumer_Key'],
                      consumer_secret=secrets['Consumer_Secret'],
                      access_token_key=secrets['Access_Token'],
                      access_token_secret=secrets['Access_Token_Secret'])
    return api

def get_other_user():
    if not hasattr(get_other_user, 'name'):
        file = open('secrets', 'r')

        secrets = yaml.load_all(file)
        name = secrets['Other_User']

    return name
        

def send_message(text, image_path):
    api = get_api()

    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tweet_text = "{0} at {1} at {}".format(text, time_str)
    if image_path is None:
        
        try:
            print('Posting direct message')
            api.PostDirectMessage(
                          tweet_text,
                          user_id=get_other_user(),
                          screen_name=None)
        except BaseException:
             print("Unexpected error while sending direct message:", sys.exc_info()[0])

    else:
        file = open(image_path, 'rb')
        data = file.read()

        try:
            print('Posting direct message with image')
            media_id = api.UploadMediaSimple(data,
                          additional_owners=[get_other_user()],
                          media_category=None)
            api.PostDirectMessageWithImage(
                          tweet_text,
                          media_id=media_id,
                          user_id=get_other_user(),
                          screen_name=None)

        except BaseException:
             print("Unexpected error while sending direct message:", sys.exc_info()[0])

