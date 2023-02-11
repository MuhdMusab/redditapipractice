import requests
from models.comment import Comment

class Post:
    def __init__(self, id, title, url, content):
        self.id = id
        self.title = title
        self.url = url
        self.content = content
        self.__top_level_comments = [] 
        self.number_of_top_level_comments = 0

    def set_top_level_comments(self, comment_list):
        self.top_level_comments = comment_list
        self.number_of_top_level_comments = len(comment_list)

    def get_comments_from_post(self, headers):
        if self.__top_level_comments:
            return self.__top_level_comments
        else:
            api_url = f"https://oauth.{self.url[12:]}"
            res = requests.get(api_url, headers=headers)
            full_json = res.json()
            comments_json = full_json[1]
            comment_list = []

            for comment_json in comments_json['data']['children']:
                url = f"https://reddit.com{comment_json['data']['permalink']}"
                comment = Comment(comment_json['data']['id'], url, comment_json['data']['body'], comment_json['data']['replies'])
                comment_list.append(comment)
            self.set_top_level_comments(comment_list)
            return comment_list