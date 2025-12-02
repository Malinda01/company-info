from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Flas setup for backend API
app = Flask(__name__)
CORS(app)

# Google sheets
SHEET_ID = "1_gL95CGnA_-TSOz-PkQ2_Rv1BqsNSM2UoJlQN1sTY9o"
SERVICE_ACCOUNT_FILE = "credentials.json"

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()


# SERPER config
SERPER_API_KEY = "2212d5a6551ac32648c69738efe8f5b368266c8b"
SERPER_URL = "https://google.serper.dev/search"


# Function to search the company details
def search_company(company):
    payload = {"q": company + " company profile", "num": 10}
    headers = {"X-API-KEY": SERPER_API_KEY}

    info = {
        "company": company,
        "founded": "",
        "location": "",
        "phone": "",
        "website": "",
    }

    try:
        res = requests.post(SERPER_URL, json=payload, headers=headers)
        data = res.json()

        # Knowledge Graph (priority)
        kg = data.get("knowledgeGraph", {})
        info["website"] = kg.get("website", "")
        info["location"] = kg.get("address", "")
        info["phone"] = kg.get("phone", "")
        info["founded"] = kg.get("foundingDate", "")

        # 2️⃣ Fallback: organic search snippets
        if "organic" in data:
            for result in data["organic"]:
                snippet = result.get("snippet", "")

                # founded year from regex
                if not info["founded"]:
                    import re

                    match = re.search(
                        r"(founded|established)\s+in\s+(\d{4})", snippet.lower()
                    )
                    if match:
                        info["founded"] = match.group(2)

                # phone from regex
                if not info["phone"]:
                    phone_match = re.search(r"(\+?\d[\d \-\(\)]{7,}\d)", snippet)
                    if phone_match:
                        info["phone"] = phone_match.group(1)

                # location
                if not info["location"]:
                    loc_match = re.search(r"in\s+([A-Z][a-zA-Z ,\-]+)", snippet)
                    if loc_match:
                        info["location"] = loc_match.group(1)

                # stop early if all fields found
                if info["founded"] and info["phone"] and info["location"]:
                    break

        # Fallback
        if not info["website"] and "organic" in data and len(data["organic"]) > 0:
            info["website"] = data["organic"][0].get("link", "")

    except Exception as e:
        print(f"Error searching {company}: {e}")
        # return at least company name
        return {
            "company": company,
            "founded": "",
            "location": "",
            "phone": "",
            "website": "",
        }

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
        write_to_sheet(data)  # save to sheet
        output.append(data)  # return to frontend

    return jsonify({"status": "success", "data": output})


if __name__ == "__main__":
    app.run(debug=True)
