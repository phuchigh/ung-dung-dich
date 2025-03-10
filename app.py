from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os
import time
import glob

app = Flask(__name__)
translator = Translator()

# Tập dữ liệu gợi ý câu
sample_sentences = {
    "chào": ["Chào bạn!", "Xin chào!", "Chào buổi sáng!"],
    "học": ["Bạn đang học gì?", "Học hành thế nào rồi?", "Học có vui không?"],
    "du lịch": ["Bạn muốn đi du lịch ở đâu?", "Địa điểm du lịch yêu thích của bạn là gì?", "Du lịch mùa hè thật thú vị!"]
}

# Hàm xóa các file âm thanh cũ
def cleanup_old_files():
    files = glob.glob("static/speech_*.mp3")
    for file in files:
        os.remove(file)

@app.route('/', methods=['GET', 'POST'])
def home():
    translated_text = ""
    suggestions = []
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        text_to_translate = request.form.get('text', "")
        source_lang = request.form['source']
        dest_lang = request.form['destination']
        
        # Dịch văn bản
        if text_to_translate:
            translated = translator.translate(text_to_translate, src=source_lang, dest=dest_lang)
            translated_text = translated.text

            # Gợi ý câu dựa trên từ khóa
            for key, value in sample_sentences.items():
                if key in text_to_translate.lower():
                    suggestions = value
                    break
    
    # Truyền kết quả dịch và gợi ý câu về giao diện
    return render_template('index.html', translated_text=translated_text, suggestions=suggestions)

@app.route('/speak', methods=['POST'])
def speak():
    cleanup_old_files()  # Xóa file âm thanh cũ trước khi tạo file mới

    text_to_speak = request.form.get('text_to_speak', "")
    print(f"Văn bản cần phát âm: {text_to_speak}")  # Ghi log văn bản đầu vào

    if not text_to_speak:
        print("Lỗi: Không có nội dung để phát âm.")  # Log lỗi
        return "Không có nội dung để phát âm", 400  # Trả về lỗi nếu nội dung trống

    try:
        # Tạo tên file duy nhất dựa trên thời gian
        timestamp = int(time.time())
        file_name = f"speech_{timestamp}.mp3"
        file_path = f"static/{file_name}"
        print(f"Đường dẫn file âm thanh: {file_path}")  # Ghi log đường dẫn file

        # Tạo file âm thanh
        tts = gTTS(text=text_to_speak, lang='en')
        tts.save(file_path)
        print("Tạo file âm thanh thành công.")  # Log thành công

        # Trả về đường dẫn file âm thanh
        return jsonify({"file_url": f"/static/{file_name}"})
    except Exception as e:
        print(f"Lỗi phát âm: {e}")  # Ghi log chi tiết lỗi
        return "Đã xảy ra lỗi trong quá trình phát âm", 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Lấy cổng từ biến môi trường (hoặc mặc định là 5000)
    app.run(host='0.0.0.0', port=port)
