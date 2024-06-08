import gspread
from oauth2client.service_account import ServiceAccountCredentials


def push_to_google_sheet(data):
    try:
        scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials/gsheet.json", scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1OfvbuAM6f7lTmn_43XNrfi5DV50epF4FNcPpxlhYWt4/edit#gid=0")
        worksheet = sheet.get_worksheet(0)
        worksheet.clear()
        values = [[data["form_id"]]]
        values.append(["Question", "Answer"])
        for question in data["questions"]:
            values.append([question["question"]] + question["answers"])
        worksheet.append_rows(values)
        print("gsheet updated")
    except Exception as e:
        print(f"An error occurred while pushing data to Google Sheets: {str(e)}")
