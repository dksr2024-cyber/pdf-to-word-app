from flask import Flask, request, send_file, render_template
import aspose.words as aw  # ប្រើប្រាស់ aspose-words ជំនួស pdf2docx
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ទិន្នន័យភាសា (Translations) សម្រាប់ប្រើប្រាស់ពីរភាសា
LANGUAGES = {
    'km': {
        'title': 'បម្លែង PDF ទៅ Word លឿន និងឥតគិតថ្លៃ',
        'header': 'បម្លែងឯកសារ PDF ទៅជា Word',
        'instruction': 'សូមជ្រើសរើសឯកសារ PDF របស់អ្នកនៅទីនេះ',
        'convert_btn': 'បម្លែងឥឡូវនេះ',
        'loading': 'កំពុងបម្លែងឯកសារ សូមរង់ចាំបន្តិច...',
        'support_header': 'គាំទ្រការបង្កើតកម្មវិធីនេះ ☕',
        'support_text': 'ប្រសិនបើកម្មវិធីនេះមានប្រយោជន៍សម្រាប់អ្នក លោកអ្នកអាចចូលរួមឧបត្ថម្ភដើម្បីជួយផ្គត់ផ្គង់ថ្លៃ Server តាមរយៈ QR Code ឬលេខគណនីរបស់ខ្ញុំខាងក្រោម សូមអរគុណ!៖',
        'account': 'គណនី ABA:',
        'error_no_file': 'សូមជ្រើសរើសឯកសារ PDF',
        'error_empty': 'មិនមានឯកសារត្រូវបានជ្រើសរើសទេ',
        'error_convert': 'មានបញ្ហាក្នុងការបម្លែងឯកសារ៖ '
    },
    'en': {
        'title': 'Fast & Free PDF to Word Converter',
        'header': 'Convert PDF to Word',
        'instruction': 'Please select your PDF file here',
        'convert_btn': 'Convert Now',
        'loading': 'Converting file, please wait...',
        'support_header': 'Support This App ☕',
        'support_text': 'If you find this app useful, you can support server costs via the QR Code or account number below. Thank you!',
        'account': 'ABA Account:',
        'error_no_file': 'Please select a PDF file',
        'error_empty': 'No file selected',
        'error_convert': 'Error during conversion: '
    }
}

@app.route('/')
def index():
    # ទាញយកភាសាពី URL (ឧទាហរណ៍: /?lang=en) បើមិនមានទេ យក 'km' ជាភាសាដើម
    lang = request.args.get('lang', 'km')
    if lang not in LANGUAGES:
        lang = 'km'
    
    # ទាញយកអត្ថបទទៅតាមភាសាដែលបានរើស រួចបញ្ជូនទៅ HTML
    text = LANGUAGES[lang]
    return render_template('index.html', text=text, current_lang=lang)

@app.route('/convert', methods=['POST'])
def convert():
    # ចាប់យកភាសាដែលបានបញ្ជូនពីទម្រង់ Form ដើម្បីបង្ហាញ Error ជាភាសាត្រឹមត្រូវ
    lang = request.form.get('lang', 'km')
    text = LANGUAGES.get(lang, LANGUAGES['km'])

    # ពិនិត្យមើលថាតើមានការបញ្ជូនឯកសារមកឬទេ
    if 'pdf_file' not in request.files:
        return text['error_no_file'], 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return text['error_empty'], 400

    # រៀបចំទីតាំងរក្សាទុកឯកសារ
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    docx_filename = file.filename.rsplit('.', 1)[0] + '.docx'
    docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)

    # រក្សាទុកឯកសារ PDF បណ្ដោះអាសន្ន
    file.save(pdf_path)

    try:
        # ការបម្លែងឯកសារដោយប្រើប្រាស់ Aspose.Words 
        doc = aw.Document(pdf_path)
        doc.save(docx_path)

        # លុបឯកសារ PDF ចោលវិញដើម្បីសន្សំទំហំផ្ទុក
        os.remove(pdf_path)
        
        # បញ្ជូនឯកសារ Word ត្រឡប់ទៅឲ្យអ្នកប្រើប្រាស់វិញ
        return send_file(docx_path, as_attachment=True)
    except Exception as e:
        return f"{text['error_convert']} {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)