from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)
CORS(app)

# Load Google Sheets Client
SHEET_ID = "YOUR_SHEET_ID"
SERVICE_ACCOUNT_FILE = "credentials.json"

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# Serper API
SERPER_API_KEY = "2212d5a6551ac32648c69738efe8f5b368266c8b"
SERPER_URL = "https://google.serper.dev/search"


def search_company(company_name):
    """Search and extract company info using Serper"""
    payload = {"q": company_name}
    headers = {"X-API-KEY": SERPER_API_KEY}

    res = requests.post(SERPER_URL, json=payload, headers=headers)
    data = res.json()

    info = {
        "company": company_name,
        "founded": "",
        "location": "",
        "phone": "",
        "website": "",
    }

    # First result information
    if "organic" in data and len(data["organic"]) > 0:
        result = data["organic"][0]

        info["website"] = result.get("link", "")

        snippet = result.get("snippet", "")

        # Very simple extraction
        if "founded" in snippet.lower():
            info["founded"] = snippet

        if "phone" in snippet.lower() or "tel" in snippet.lower():
            info["phone"] = snippet

        if "address" in snippet.lower() or "located" in snippet.lower():
            info["location"] = snippet

    return info


def write_to_sheet(row):
    values = [
        [row["company"], row["founded"], row["location"], row["phone"], row["website"]]
    ]

    sheet.values().append(
        spreadsheetId=SHEET_ID,
        range="Sheet1!A:E",
        valueInputOption="RAW",
        body={"values": values},
    ).execute()


@app.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    df = pd.read_csv(file)

    companies = df[df.columns[0]].tolist()

    output = []

    for c in companies:
        data = search_company(c)
        write_to_sheet(data)
        output.append(data)

    return jsonify({"status": "success", "data": output})


if __name__ == "__main__":
    app.run(debug=True)
