from flask import Flask, request, send_file, render_template
from pdf2docx import Converter
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # ពិនិត្យមើលថាតើមានការបញ្ជូនឯកសារមកឬទេ
    if 'pdf_file' not in request.files:
        return "សូមជ្រើសរើសឯកសារ PDF", 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return "មិនមានឯកសារត្រូវបានជ្រើសរើសទេ", 400

    # រៀបចំទីតាំងរក្សាទុកឯកសារ
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    docx_filename = file.filename.rsplit('.', 1)[0] + '.docx'
    docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)

    # រក្សាទុកឯកសារ PDF បណ្ដោះអាសន្ន
    file.save(pdf_path)

    try:
        # បម្លែង PDF ទៅជា Word
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        # លុបឯកសារ PDF ចោលវិញដើម្បីកុំឱ្យពេញទំហំផ្ទុក
        os.remove(pdf_path)

        # បញ្ជូនឯកសារ Word ឱ្យអ្នកប្រើប្រាស់ទាញយក
        return send_file(docx_path, as_attachment=True)
    except Exception as e:
        return f"មានបញ្ហាក្នុងការបម្លែងឯកសារ៖ {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)