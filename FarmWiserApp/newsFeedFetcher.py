import feedparser
import datetime
from newspaper.nlp import summarize
from requests.utils import quote
from newspaper import Article
import newspaper
from enum import Enum
import nltk

nltk.download("punkt")


SEARCH_URL = (
    "https://news.google.com/rss/search?q={}&hl=en-IN&gl=IN&ceid=IN:en&sort=date"
)
TOPIC_URL = (
    "https://news.google.com/rss/topics/{id}?hl=en-IN&gl=IN&ceid=IN:en&sort=date"
)


class TOPICS(Enum):
    AGRICULTURE = "CAAqJAgKIh5DQkFTRUFvSEwyMHZNR2hyWmhJRlpXNHRSMElvQUFQAQ"


def sort_news(news_list):
    return news_list["entries"].sort(
        key=lambda entry: entry["published_parsed"], reverse=True
    )


def news_by_topic(topic: TOPICS):
    news = feedparser.parse(TOPIC_URL.format(id=topic.value))
    sort_news(news)
    return [
        {
            "title": entry["title"],
            "link": entry["link"],
            "published": entry["published"],
            "timestamp": int(
                datetime.datetime(
                    *(entry["published_parsed"][:7]), tzinfo=datetime.timezone.utc
                ).timestamp()
            ),
        }
        for entry in news["entries"]
    ]


def search_news(query):
    news = feedparser.parse(SEARCH_URL.format(quote(query)))
    sort_news(news)
    return [
        {
            "title": entry["title"],
            "link": entry["link"],
            "published": entry["published"],
            "timestamp": int(
                datetime.datetime(
                    *(entry["published_parsed"][:7]), tzinfo=datetime.timezone.utc
                ).timestamp()
            ),
        }
        for entry in news["entries"]
    ]


def get_image(news_url):
    article = Article(news_url)
    article.download()
    article.parse()
    return {"image_url": article.top_image}


def get_article(news_url):
    content = newspaper.Article(url="%s" % (news_url), language="en")
    content.download()
    content.parse()
    content.nlp()

    title = content.title

    published = content.publish_date

    text_string = content.text

    summary_text = content.summary.replace("\n", " ")

    fullText_string = f"{text_string}"

    fullText = (
        fullText_string.replace("\n", "")
        .replace("/", "")
        .replace(". ", "./")
        .split("/")
    )

    items = {
        "link": news_url,
        "title": title,
        "published": published,
        "full_text": fullText,
        "summary": summary_text,
    }

    return items
