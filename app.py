from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def home():
    translated_text = ""
    if request.method == 'POST':
        text_to_translate = request.form['text']
        source_lang = request.form['source']
        dest_lang = request.form['destination']
        translated = translator.translate(text_to_translate, src=source_lang, dest=dest_lang)
        translated_text = translated.text
    return render_template('index.html', translated_text=translated_text)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Lấy cổng từ biến môi trường (hoặc mặc định là 5000)
    app.run(host='0.0.0.0', port=port)
