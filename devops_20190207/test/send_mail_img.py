#!/usr/bin/env python
# coding: utf-8
'''
@author: duoyichen
@email: duoyichen@qq.com
@date:  
'''

# !/usr/bin/python
# coding=utf-8

import sys
import time
import os

HOME = "/usr/local/scripts/idcmail"


def build_mail(subject, content, address_to, Ccs, images, attachment):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage

    # msgRoot = MIMEMultipart('related')
    msgRoot = MIMEMultipart('alternative')
    msgRoot['Subject'] = subject
    msgRoot['From'] = "robot@dnion.com"
    msgRoot['To'] = address_to
    msgRoot['Cc'] = Ccs
    _my_time = time.strftime('%a, %d %b %Y %H:%M:%S +0800 (CST)', time.localtime(time.time()))
    msgRoot['Date'] = _my_time

    suffix = """
    <img src="cid:logo" alt="logo">
    北京易网信科技发展有限公司 
    Add： 西城区北三环中路27号商房大厦5层 531室
    全国统一客服热线：4009280260
    7*24小时受理邮箱:idccs@51ywx.com
    """

    html = """
    <html> 
      <head></head> 
      <body> 
          <p>
           %s
           <br><img src="cid:peace" alt="peace"></br> 
            %s
          </p>
      </body> 
    </html> 
    """ % (content, suffix.replace('\n', '</br>'))

    full_msg = MIMEText(html, 'html', 'utf-8')  # 这个关键字使得可以发送html作为正文
    msgRoot.attach(full_msg)

    fp = open(HOME + '/' + images, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<peace>')
    msgRoot.attach(img)

    fp2 = open(HOME + '/logo.jpg', 'rb')
    img2 = MIMEImage(fp2.read())
    fp2.close()
    img2.add_header('Content-ID', '<logo>')
    msgRoot.attach(img2)

    if attachment:
        att1 = MIMEText(open(HOME + '/123.txt', 'rb').read(), 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="123.txt"'  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        # msgRoot.attach(att1)
    return msgRoot


def send_mail(subject, content, address_to, Ccs, images, attachment=False):
    import smtplib
    smtp = smtplib.SMTP()
    smtp.connect("122.11.61.70", 25)
    # smtp.set_debuglevel(1)
    smtp.login("robot", "XbLKzpQ40bznIC7s")
    mailbody = build_mail(subject, content, address_to, Ccs, images, attachment)
    # print mailbody
    address_to += ";chenying@51ywx.com"
    smtp.sendmail("robot@dnion.com", address_to.split(';'), mailbody.as_string())
    smtp.quit()


if __name__ == "__main__":
    import optparse

    # USAGE = 'python %prog  <--subject=subject> [--content=mailbody]|[--file=filename] [--to=reciver].\n\nexample: %prog --to="friends1@domain.com -s "Hello from MailViaSMTP" -c "This is a mail just for testing."'
    USAGE = 'python sendmail_img.py  -n new'
    VERSION = '%prog 1.0'
    DESC = u"""This is a command line kit for sending mail via smtp server which can use in multiple platforms like linux, BSD, Windows etc. This little kit was written by leopku@qq.com using python. The minimum version of python required was 2.3."""

    parser = optparse.OptionParser(usage=USAGE, version=VERSION, description=DESC)
    # parser.add_option('-s', '--subject', help='The subject of the mail.')
    parser.add_option('-n', '--sendnew',
                      help='Give the new flag,modify program with subject,suffix;fill the mailcontent.txt')
    parser.add_option('-t', '--to', dest='address_to', metavar='friend@domain2.com',
                      help='Set recipient address. Use semicolon to seperate multi recipient, for example: "a@a.com;b@b.com."')
    parser.add_option('-A', '--attachment', dest='attachment', help='if not empty,means we will send attachment')
    # parser.add_option('-F', '--file', dest='file', help='Read mail body from file. NOTE:  --file will be ignored if work with --content option at same tome.')
    # parser.add_option('-p', '--pic', dest='picture', help='Image with full suffix to be send as mailbody,only pic name is enough!')
    opts, args = parser.parse_args()

    if not opts.sendnew:
        sys.exit(u"""请确认已经改好附件-程序与外部内容，收件人sql-程序，邮件正文-外部内容，标题-程序, 图片-程序与外部内容
Example:python sendmail_img.py -n "xx" -t "duoyichen@qq.com"  -A "yes";""")

    subject = "【易网信】新年快乐!"

    content = ""
    fp = open(HOME + '/mailcontent.txt', 'r')
    for line in fp:
        content += line + '</br>'
    fp.close()
    # picture="danian.png"
    picture = "new_year_2019.jpg"

    attachment = False
    if opts.attachment:
        attachment = True
    Ccs = "chenying@51ywx.com"

    import pymysql

    conn = pymysql.connect(host='122.11.50.35', user='emidc', db='easymonitord',
                           password='dja9sdhasdasndoia)asdjaisd9)sa_fxsajs', port=3306, use_unicode=True,
                           charset="utf8")
    cur = conn.cursor()
    sql = "select custName,linkEmails from easy_idc_custEmail where custName like '%send' group by linkEmails"
    cur.execute(sql)
    if cur.rowcount == 0:
        sys.exit("sql return no customer emails!")
    for row in cur.fetchall():
        cust, email = (row[0], row[1].replace(',', ';'))
        # print "sending to "+email;
        try:
            print("haha")
            # send_mail(subject, content, email, Ccs, picture, attachment)
            # send_mail(subject, content, email, Ccs, picture)
        except:
            print
            "sending to " + email + " fail"
    conn.close()

    # send_mail(subject, content, opts.address_to, Ccs, picture, attachment)
    # send_mail(subject, content, opts.address_to, Ccs, picture)
    # fp = open(HOME+'/mailcontent.txt', 'w')
    # fp.truncate()
    # fp.close()