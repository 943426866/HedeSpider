from flask import Flask, request
from threading import Thread
import os
import time
app = Flask(__name__)


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
 
    return wrapper


@async
def scrapydoc(key_dict):
    scrapy_shell = 'scrapy crawlall'
    for key in key_dict:
        scrapy_shell += ' -a '+key+'="'+key_dict[key]+'"'
    os.system(scrapy_shell)


@app.route('/start_crawl')
def start_crawl():
    scrapydoc(request.args.to_dict())
    return str("success")


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(threaded=True)
