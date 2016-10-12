# consolidate.py
# This script will take in all the generated json files with the pca_test results and add it to an excel file

from tinydb import TinyDB, Query
import sys as Sys
file_name = Sys.argv[1]
db = TinyDB(file_name)
row = raw_input("What row?: ")
count = 1

def authorize_gsheets(credentials_file,url):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    gc = gspread.authorize(credentials)
    
    #sh = gc.open_by_url(url)
    worksheet = gc.open('pca_tests_data').sheet1
    return worksheet

credentials_file = 'block-ca-caf120fef8db.json'
url = "https://docs.google.com/spreadsheets/d/1EFTsd8IN7WFHjcXCTu7_dlG2J_eVg-chp80u45h0roc/edit#gid=0"
worksheet = authorize_gsheets(credentials_file, url)

for test in db.all():
	for x in test.items():
		name, value = x
		worksheet.update_cell(row, count, name)
		worksheet.update_cell(int(row) + 1, count, str(value))
		count += 1



