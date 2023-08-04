from weasyprint import CSS, HTML

HTML('http://samplewebsite.com/').write_pdf('/home/leonardo/Downloads/test.pdf', stylesheets=[CSS(string='body { font-size: 10px }')])
