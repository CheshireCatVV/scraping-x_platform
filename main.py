import json
import os
import ast

from dotenv import load_dotenv

from playwright.sync_api import sync_playwright

from parser_classes import ProfileDataParser, TweetDataParser


def get_page_response_json(page, response_part: str, wait_for_data_el: str) -> json:
    with page.expect_response(response_part) as response_info:
        page.wait_for_selector(wait_for_data_el)
        return response_info.value.json()


def main():
    with sync_playwright() as pw:
        page = pw.chromium.launch()
        page = page.new_page()
        page.goto(profile_url)

        response_json_data = get_page_response_json(page=page, response_part=profile_response_part,
                                                    wait_for_data_el=wait_for_profile_data_el)
        json_data = profile_data_parser.get_data_by_keys_order(json_data=response_json_data,
                                                               keys_order=profile_data_keys_order)
        scraped_data["profile_data"] = profile_data_parser.parse_json_data(json_data=json_data, profile_url=profile_url)

        tweets_list = list()

        response_json_data = get_page_response_json(page=page, response_part=tweets_response_part,
                                                    wait_for_data_el=wait_for_tweet_data_el)
        json_data = tweet_data_parser.get_data_by_keys_order(json_data=response_json_data,
                                                             keys_order=pined_tweet_key_order)
        json_data = tweet_data_parser.get_data_by_keys_order(json_data=json_data, keys_order=tweet_data_key_order)
        pinned_tweet = tweet_data_parser.parse_json_data(json_data=json_data)
        tweets_list.append(pinned_tweet)

        for json_data in tweet_data_parser.get_data_by_keys_order(json_data=response_json_data,
                                                                  keys_order=tweets_key_order):
            json_data = tweet_data_parser.get_data_by_keys_order(json_data=json_data,
                                                                 keys_order=tweet_data_key_order)
            tweets_list.append(tweet_data_parser.parse_json_data(json_data=json_data))

        scraped_data["tweets"] = tweets_list[:tweets_slice_num]


if __name__ == '__main__':
    load_dotenv()
    profile_url = os.getenv("PROFILE_URL")
    profile_response_part = os.getenv("PROFILE_RESPONSE_PART")
    wait_for_profile_data_el = os.getenv("WAIT_FOR_PROFILE_DATA_ELEMENT")
    profile_data_keys_order = ast.literal_eval(os.getenv("PROFILE_DATA_KEYS_ORDER"))

    pined_tweet_key_order = ast.literal_eval(os.getenv("PINED_TWEET_KEY_ORDER"))
    tweets_response_part = os.getenv("TWEETS_RESPONSE_PART")
    wait_for_tweet_data_el = os.getenv("WAIT_FOR_TWEET_DATA_ELEMENT")
    tweets_key_order = ast.literal_eval(os.getenv("TWEETS_KEY_ORDER"))
    tweet_data_key_order = ast.literal_eval(os.getenv("TWEET_DATA_KEY_ORDER"))
    tweets_slice_num = ast.literal_eval(os.getenv("TWEETS_SLICE_NUM"))

    profile_data_parser = ProfileDataParser()
    tweet_data_parser = TweetDataParser()
    scraped_data = dict()
    main()

    with open("scraped_data.json", "w") as f:
        f.write(json.dumps(scraped_data, indent=4, sort_keys=True))
