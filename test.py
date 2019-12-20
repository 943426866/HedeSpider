import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r'wkhtmltox/bin/wkhtmltopdf.exe')


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
    path = 'd:/projectfile/smolib/pdf/test_pdf/title.pdf'
    try:
        pdfkit.from_string(html, path, configuration=config)
    except Exception as e:
        print(e)


html2pdf('title', 'content', 'pdf\\test_pdf')
