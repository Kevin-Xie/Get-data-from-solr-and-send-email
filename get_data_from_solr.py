# -*- coding: utf-8 -*-
import urllib2
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SOLR_URL = 'http://xxxxxxxxxxxxxx/select?q=MsgType_s%3A+%22BC%22&sort=EventGMT_dt+DESC&start=0&rows=20&wt=csv&indent=true'
SOLR_AUTH_USER = '******'
SOLR_AUTH_PASSWORD = '******'


emailConfig = {
	'From': 'xxx@xxx.com',
	'To': 'yyy@yyy.com',
	'Subject': 'data from Solr',
	'Body':'email body',
	'attachments': []	# [('filename1', 'data1'), ('filename2', 'data2')]
}


def generateAndSendReport():
	content = getDataFromSolr(SOLR_URL)
	initEmailAttachments([(generateFileName(), content)])
	email = setupEmailMessage(emailConfig)
	sendEmailMessage(email)


def getDataFromSolr(url):
	pwdMan = urllib2.HTTPPasswordMgrWithDefaultRealm()
	pwdMan.add_password(None, 'solrprod.cargosmart.org', SOLR_AUTH_USER, SOLR_AUTH_PASSWORD)
	auth_handler = urllib2.HTTPBasicAuthHandler(pwdMan)
	opener = urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)
	return urllib2.urlopen(url).read()


def saveDataToCSV(content, fileName):
	with open(fileName, 'wb') as file:
		file.write(content)


def generateFileName():
	return 'result_' + time.strftime('%Y_%m_%d', time.localtime()) + '.csv'


def initEmailAttachments(items):
	emailConfig['attachments'] = []
	for item in items:
		emailConfig['attachments'].append(item)


def initEmailSender(host='SMTPAPP1'):
	return smtplib.SMTP(host)


def setupEmailMessage(email):
	msg = MIMEMultipart()
	msg['From'] = email['From']
	msg['To'] = email['To']
	msg['Subject'] = email['Subject']
	msg.attach(MIMEText(email['Body'], 'plain', 'utf-8'))
	for name, attachment in email['attachments']:
		msg.attach(MIMEApplication(attachment, name=name))
	return msg


def sendEmailMessage(msg):
	sender = initEmailSender()
	sender.sendmail(msg['From'] , msg['To'] , msg.as_string())
	sender.quit()


def main():
	generateAndSendReport()

if __name__ == '__main__':
	main()