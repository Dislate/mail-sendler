import smtplib
import mimetypes
import os
import json
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

class Server:
    def __init__(self):
        self.accounts = self.read_accounts()
        self.adress_book = AdressBook()
        print(self.accounts, self.adress_book, sep='\n')

    def read_config(self, config='config.json'):
        with open(config) as cf:
            config = json.load(cf)
            cf.close()
            return config
    
    def update_config(self, config_variable, config='config.json'):
        with open(config, 'w') as cf:
            json.dump(config_variable, cf, indent=4)
            cf.close()

    def read_accounts(self):
        config = self.read_config()
        try:
            accounts = [AccountMail(i['email'], i['password'], i) for i in config['emails']]
        except:
            accounts = []
        return accounts

    def read_adressbook(self):
        config = self.read_config()
        categories = []
        try:
            config['adressbook']
        except:
            config['addressbook'] = {
                "All": {}
            }
            return categories.append([Category(i) for i in self.categories.keys()])
        else:
            for i in config['adressbook'].keys():
                categories.append(Category(i))
            return categories
            
    def add_account(self, email, password):
        config = self.read_config()
        config['emails'].append(dict([('email', email), ('password', password)]))
        self.accounts.append(AccountMail(email, password, dict(config['emails'][-1])))
        self.update_config(config)
        print(self.accounts)
        print('Account added')

    def attach_file(self, msg, filepath):
        print(filepath)
        filename = os.path.basename(filepath)
        ftype, encoding = mimetypes.guess_type(filepath)
        if ftype is None or encoding is not None:
            ftype = 'application/octet-stream'
        maintype, subtype = ftype.split('/', 1)
        if maintype == 'text':
            with open(filepath) as fp:
                file = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
        elif maintype == 'image':
            with open(filepath, 'rb') as fp:
                file = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
        else:
            with open(filepath, 'rb') as fp:
                file= MIMEBase(maintype, subtype)
                file.set_payload(fp.read())
                fp.close()
            encoders.encode_base64(file)
        file.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(file)

    def process_attachment(self, msg, files):
        for f in files:
            if os.path.isfile(f):
                self.attach_file(msg, f)
            elif os.path.exists(f):
                dir = os.listdir(f)
                for file in dir:
                    self.attach_file(msg, f + '/' + file)

class AccountMail(Server):
    def __init__(self, email, password, config_email):
        self.email = email
        self.password = password
        self.config_email = config_email
       
    def send_mail(self, emails, message_subject, message_text, files=None):
        email = self.email
        password = self.password   

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = emails
        msg['Subject'] = message_subject

        body = message_text
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        if files != None:
            self.process_attachment(msg, files)
        
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.login(email, password)

        server.send_message(msg)

        server.quit()
    
    def __repr__(self):
        return f'<{self.email}: {self.password}>'

class AdressBook(Server):
    def __init__(self):
        self.categories = self.read_adressbook()

    def add_category(self, name):
        self.categories.append(Category(name))
        config = self.read_config()
        config['adressbook'][name] = {}
        self.update_config(config)

    def __repr__(self):
        return 'Категории: ' + ', '.join([i.name for i in self.categories])
    # def read_categories(self, config)

class Category(AdressBook):
    def __init__(self, name):
        self.name = name
        self.emails = []

    def add_email(self, namecompany, email):
        self.emails.append(Email(namecompany, email))

    def remove_email(self, emailobj):
        self.email.remove(emailobj)

    # def import_contacts(self, filepath):

filepath = [r'/mnt/98CC0D12CC0CEC76/DjangoProjects/mail-sendler/new']

if __name__ == '__main__':
    x = Server()
    x.accounts[0].send_mail('recipients is str', 'Testsubject', 'TestText', filepath)