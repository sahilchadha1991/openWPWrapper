# Writing a wrapper for WP Scan

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
import subprocess
import shlex
import hashlib
import smtplib
import os


hashedFileDict = {}


def removeCookieFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def readWordPressSites(files):
    wordpressSiteList = [site.strip('\n')
                         for site in open(files)]
    return wordpressSiteList


# ruby wpscan.rb --url https://stylestories.ebay.com --log stylestories
def runWPScan():
    removeCookieFile('./wpscan/cache/browser/cookie-jar')
    siteList = readWordPressSites('wordpressSites.txt')
    print siteList
    processList = []
    commands = ['ruby ./wpscan/wpscan.rb --url ' + site + ' --batch' +
                ' --follow-redirection' + ' --random-agent' + ' --no-color'
                ' --no-banner'
                for site in siteList]

    for command in commands:
        args = shlex.split(command)
        print args[3]
        fileName = hashlib.sha256(args[3]).hexdigest()
        hashedFileDict[args[3]] = fileName
        print fileName
        fileName = './results/' + fileName + '.txt'
        log = open(fileName, 'w+')
        processList.append(subprocess.Popen(args, stdout=log))

    exitCode = [p.wait() for p in processList]
    print exitCode
    print "Execution finished"
    print hashedFileDict
    # sendResults(hashedFileDict)
    sendResults()


def sendResults():
    for key, attachmentFile in hashedFileDict.iteritems():
        attachmentPath = open('./results/' + attachmentFile + '.txt', "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachmentPath).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s"
                        % attachmentFile)
        msg = MIMEMultipart()
        msg.attach(part)
        msg['Subject'] = 'Wordpress Issues in ' + key
        msg['From'] = 'SPLC_bot@ebay.com'
        msg['To'] = 'sachadha@ebay.com'
        body = ("Hi,\n\n We scanned your wordpress sites for issues, "
                "and we have attached the "
                "issues found with this email. Please fix these issues "
                "as soon as possible.\n\n Regards, \n SPLC Team")
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('atom.corp.ebay.com', 25)
        text = msg.as_string()
        print server.starttls()
        print server.sendmail("SPLC_bot@ebay.com", "sachadha@ebay.com",
                              text)
        server.quit()



runWPScan()
