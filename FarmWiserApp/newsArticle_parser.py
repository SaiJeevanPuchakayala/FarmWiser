"""
Author: Sai Jeevan Puchakayala
"""
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from datetime import datetime
from newspaper import Article
import newspaper
import nltk

nltk.download("punkt")

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "english"
SENTENCES_COUNT = 2


def get_image(news_url):
    article = Article(news_url)
    article.download()
    article.parse()
    return article.top_image


def get_summary(news_url):
    parser = HtmlParser.from_url(news_url, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    complete_sentence = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        complete_sentence = complete_sentence + str(sentence)
    return (
        complete_sentence.replace("“", "")
        .replace("” ", " ")
        .replace("”", "")
        .replace(".", ". ")
    )


def get_article(news_url, news_timestamp, news_source):
    items = {
        "banner_link": "-",
        "url": "-",
        "title": "-",
        "sourcelink": "-",
        "createdAt": "-",
        "createdAt_unix": "-",
        "backend_parameter": "-",
        "content": "-",
    }
    try:
        content = newspaper.Article(url="%s" % (news_url), language="en")
        content.download()
        content.parse()
        content.nlp()

        title = content.title

        published = content.publish_date

        date = str(datetime.now()).split(" ")[0]

        items = {
            "banner_link": get_image(news_url),
            "url": news_url,
            "title": title,
            "sourcelink": news_source,
            "createdAt": published,
            "createdAt_unix": news_timestamp,
            "backend_parameter": date,
            "content": get_summary(news_url),
        }
    except Exception:
        pass

    return items
