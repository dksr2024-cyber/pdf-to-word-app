# ប្រើប្រាស់ Python 3.12 ជំនាន់ស្រាលជាមូលដ្ឋាន
FROM python:3.12-slim

# ដំឡើងបណ្ណាល័យប្រព័ន្ធ ព្រមទាំងដំឡើង "ហ្វុន្តខ្មែរ" ចូលទៅក្នុង Server ផ្ទាល់!
RUN apt-get update && apt-get install -y \
    libfontconfig1 \
    libicu-dev \
    fonts-khmeros \
    && rm -rf /var/lib/apt/lists/*

# កំណត់ទីតាំងផ្ទុកឯកសារ
WORKDIR /app

# ចម្លងកូដទាំងអស់របស់បងចូលទៅក្នុង Server
COPY . /app

# ដំឡើងបណ្ណាល័យ Python (Flask, Aspose...)
RUN pip install --no-cache-dir -r requirements.txt

# បើកដំណើរការវេបសាយ (ប្រើប្រាស់ Port ដែល Render ផ្ដល់ឲ្យ)
CMD gunicorn --bind 0.0.0.0:$PORT app:app
