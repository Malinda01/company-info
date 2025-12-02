Company Data Tracker (CSV → Google Sheets)

This project allows users to upload a CSV file containing company names. The system automatically searches each company on Google using the SERPER API, extracts key details, and updates a Google Sheet in real time.

🚀 Features

Upload CSV file from React frontend

Flask backend processes company list

Fetches company info using SERPER API

Extracts website, location, phone, and founding year

Stores results directly into Google Sheets

Returns data back to frontend for display

🛠️ Tech Stack

Frontend: React

Backend: Flask (Python)

APIs: SERPER API, Google Sheets API v4

Data Store: Google Sheets

📌 How It Works

User uploads a CSV with company names.

Flask reads the CSV using pandas.

Each company name is searched using SERPER API.

Extracted details are appended to Google Sheets.

Results are returned to the frontend.

📁 CSV Format
company
Google
Apple
Microsoft

▶️ Run the Backend
pip install -r requirements.txt
python app.py

▶️ Run the Frontend
npm install
npm start

📜 Environment Variables
SERPER_API_KEY=your_key
GOOGLE_SHEET_ID=your_sheet_id
SERVICE_ACCOUNT_FILE=credentials.json
