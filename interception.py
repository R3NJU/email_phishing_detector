import smtpd
import asyncore
import smtplib
import traceback
import re
from ml_model import predict

class CustomSMTPServer(smtpd.SMTPServer):

    def detect(urls):
        for i in urls:
            if predict(i):
                return True
        return False

    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        
        message_pattern = r'\nFrom:\s\S+\s\<\S+\>\n\n(.*)'
        url_pattern = r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\-\+~#=]{2,256}\.[a-z]{2,15}\b[-a-zA-Z0-9@:%_\-\+.~#?&//=]*"

        mailfrom.replace("\'", '')
        mailfrom.replace('\"', '')
        for recipient in rcpttos:
            recipient.replace("\'", '')
            recipient.replace('\"', '')

        try:
            s_data = data.decode('utf-8')
            message = re.search(message_pattern, s_data).group(1)
            urls = re.findall(url_pattern, message)
            descision = self.detect(urls) if urls else False
            if descision:
                s_data = s_data.replace(message, '[!!!! This Email Contains Phishing URLs !!!!]\n\n'+message)
            data = str.encode(s_data)
        except:
            pass
            print('Something went wrong')
            print(traceback.format_exc())
        try:
            server = smtplib.SMTP('localhost', 10026)
            server.sendmail(mailfrom, rcpttos, data)
            server.quit()
            print('Send Successful')
        except Exception as e:
            print(e)
        return
    
server = CustomSMTPServer(('127.0.0.1', 10025), None)
asyncore.loop()