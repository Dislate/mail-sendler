import pandas as pd #parse excel file
from time import sleep 
from controllers import * #logic sendler

#parse recipients from excel files
exel_document = pd.read_excel(r'Your path', sheet_name='namesheet', usecols=['yournamecols'])
recipients = list(set([i for i in exel_document['yournamecols']]))


files = [r'pathtodictwithfiles'] #path to pinned files

while len(recipients):
    server = Server()
    server.accounts[0].send_email(', '.join(recipients[:30]), "Subject mail", 'Text mail', files)
    if len(recipients) >= 30:
        recipients = recipients[30:]
    else:
        recipients = []
    sleep(60) #interval between sending mails

    

