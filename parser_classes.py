import abc
import enum
import json


class AbstractParser(abc.ABC):
    @staticmethod
    def get_data_by_keys_order(keys_order: tuple, json_data: json):
        for key in keys_order:
            json_data = json_data[key]

        return json_data

    @abc.abstractmethod
    def parse_json_data(self, *args, **kwargs):
        pass


class ProfileDataParser(AbstractParser):
    class ProfileFields(enum.Enum):
        USERNAME = "username"
        DISPLAY_NAME = "display_name"
        FOLLOWERS = "followers"
        FOLLOWING = "following"
        TWEETS_QTY = "tweets_qty"
        PROFILE_URL = "profile_url"
        PROFILE_SMALL_IMAGE_URL = "profile_small_image_url"
        PINNED_TWEET_IDS = "pinned_tweet_ids"
        ON_SITE_SINCE = "on_site_since"
        PROFILE_DESCRIPTION = "profile_description"

    def parse_json_data(self, json_data: json, profile_url: str):
        return {
            self.ProfileFields.USERNAME.value: json_data["screen_name"],
            self.ProfileFields.DISPLAY_NAME.value: json_data["name"],
            self.ProfileFields.FOLLOWERS.value: json_data["normal_followers_count"],
            self.ProfileFields.FOLLOWING.value: json_data["friends_count"],
            self.ProfileFields.TWEETS_QTY.value: json_data["statuses_count"],
            self.ProfileFields.PROFILE_URL.value: profile_url,
            self.ProfileFields.PROFILE_SMALL_IMAGE_URL.value: json_data["profile_image_url_https"],
            self.ProfileFields.PINNED_TWEET_IDS.value: json_data["pinned_tweet_ids_str"],
            self.ProfileFields.ON_SITE_SINCE.value: json_data["created_at"],
            self.ProfileFields.PROFILE_DESCRIPTION.value: json_data["description"],
        }


class TweetDataParser(AbstractParser):
    class TweetFields(enum.Enum):
        PUBLICATION_DATE = "publication_date"
        TWEET_CONTENT_TEXT = "tweet_content_text"
        TWEET_LIKES_QTY = "tweet_likes_qty"
        QUOTE_COUNT = "quote_count"
        RETWEETS_QTY = "retweets_qty"
        REPLAYS = "replays"
        MEDIA_URLS = "media_urls"
        TWEET_ID = "tweet_id"

    def parse_json_data(self, json_data: json, ):
        data = {
            self.TweetFields.PUBLICATION_DATE.value: json_data["created_at"],
            self.TweetFields.TWEET_CONTENT_TEXT.value: json_data["full_text"].replace("\n", ""),
            self.TweetFields.TWEET_LIKES_QTY.value: json_data["favorite_count"],
            self.TweetFields.QUOTE_COUNT.value: json_data["quote_count"],
            self.TweetFields.RETWEETS_QTY.value: json_data["retweet_count"],
            self.TweetFields.REPLAYS.value: json_data["reply_count"],
            self.TweetFields.MEDIA_URLS.value: None,
            self.TweetFields.TWEET_ID.value: json_data["id_str"],
        }
        if not "media" in json_data["entities"]:
            return data

        data[self.TweetFields.MEDIA_URLS.value] = [item["media_url_https"] for item in json_data["entities"]["media"]]
        return data
