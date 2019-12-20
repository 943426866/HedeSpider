from bs4 import BeautifulSoup as bs
import time
import pdfkit
import os

config = pdfkit.configuration(wkhtmltopdf=r'wkhtmltox/bin/wkhtmltopdf.exe')


def B2Q(uchar):
    # 半角转全角
    return chr(ord(uchar)+0xfee0)


def reshape_title(title):
    prohibit_words = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for word in prohibit_words:
        title = title.replace(word, B2Q(word))
    return title


def reshape_kwargs(kwargs, key):
    try:
        keywords = kwargs[key]
    except Exception as e:
        keywords = ''
    return keywords


def reshape_content(content):
    soup = bs(content, 'lxml')
    # 清除图片
    [s.extract() for s in soup("img")]
    # 清除超链接
    [s.replace_with(s.text.strip()) for s in soup("a")]
    return soup.prettify()


def html2pdf(title, content, targetPath):
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
        </head>
        <body>
        <h2 style="text-align: center;font-weight: 400;">{title}</h2>
        {content}
        </body>
        </html>
        '''
    try:
        pdfkit.from_string(html, 'd:/projectfile/smolib/' + targetPath + f'/{title}.pdf', configuration=config)
    except Exception as e:
        print(e)


def reshape_path(spider_name):
    path = 'pdf/'+spider_name+'_pdf'
    real_path = 'd:/projectfile/smolib/'+path
    if not os.path.exists(real_path):
        os.makedirs(real_path)
    return path
