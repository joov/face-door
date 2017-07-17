import Api from twitter

class ExtApi(Api):


    def PostDirectMessageWithImage(self,
                          text,
                          media_id,
                          user_id=None,
                          screen_name=None):
        """Post a twitter direct message from the authenticated user with image.
        Args:
          text: The message text to be posted.  Must be less than 140 characters.
          user_id:
            The ID of the user who should receive the direct message. [Optional]
          screen_name:
            The screen name of the user who should receive the direct message. [Optional]
        Returns:
          A twitter.DirectMessage instance representing the message posted
        """
        url = '%s/direct_messages/new.json' % self.base_url
        data = {'text': text,
                "attachment": {
                    "type": "media",
                    "media": {
                    "id": media_id
                    }
                }
        }
        if user_id:
            data['user_id'] = user_id
        elif screen_name:
            data['screen_name'] = screen_name
        else:
            raise TwitterError({'message': "Specify at least one of user_id or screen_name."})

        resp = self._RequestUrl(url, 'POST', data=data)
        data = self._ParseAndCheckTwitter(resp.content.decode('utf-8'))

        return DirectMessage.NewFromJsonDict(data)