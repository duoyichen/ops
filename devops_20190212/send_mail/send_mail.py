#!/usr/bin/env python
# coding: utf-8
'''
@author: duoyichen
@email: duoyichen@qq.com
'''
from email.utils import make_msgid,formatdate
from email.mime.text import MIMEText    #html格式和文本格式邮件
from email.mime.multipart import MIMEMultipart    #带多个部分的邮件
from email.mime.image import MIMEImage    #带图片格式邮件
from email.mime.audio import MIMEAudio    #音频文件对象
from email.utils import formataddr    #分隔标题与地址
from email.header import Header    #设置标题字符集
from email import encoders    #编码器
from email.mime.application import MIMEApplication    #主要类型的MIME消息对象应用
from email.mime.base import MIMEBase
from fetch_mail_list import get_mail_list_from_excel
from fetch_mail_list import get_mail_list_from_mysql


# def build_msg_html_image(subject, receiver, image_body, html):
def build_msg_html_image(*args):
    '''
    用户需要依次传入 subject, receiver, html, [ image | start_time, end_time, idc_name ] 等参数，
    其他参数都是默认的，也可以在本函数中自行修改。
    '''
    # 解析参数
    subject = args[0]
    receiver = args[1]
    html = args[2]
    if len(args) == 4:
        image = args[3]
    elif len(args) == 6:
        start_time = args[3]
        end_time = args[4]
        idc_name = args[5]
    else:
        print('invalid args, please check!')
        exit(2)

    ## 下面参数请根据实际需要修改
    sender = 'robot@51ywx.com'
    # cc = ['idccs@51ywx.com']
    # bcc = ['chenying@51ywx.com']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = formataddr(['易网信Robot ', sender])
    msg['To'] = ','.join(receiver)
    # 根据实际情况决定 抄送，暗送
    # msg['Cc'] = ','.join(cc)
    # msg['Bcc'] = ','.join(bcc)
    msg['Message-id'] = make_msgid()
    msg['Date'] = formatdate(localtime=1)

    ## 下面参数请根据实际需要修改
    image_logo = "image/logo.jpg"
    image_logo_id = 'image_logo_id'
    with open(image_logo, "rb") as f:
        logo = MIMEImage(f.read())
        f.close()
    logo.add_header('Content-ID', image_logo_id)
    msg.attach(logo)

    ## 下面参数请根据实际需要修改
    html_footer = 'html_footer.txt'
    f = open(html_footer,'rb')
    html_footer = f.read().decode() %(image_logo_id)
    f.close()

    f = open(html,'rb')
    if len(args) == 4:
        image_id = 'image_id'
        with open(image, "rb") as f2:
            new_year = MIMEImage(f2.read())
            f2.close()
        new_year.add_header('Content-ID', image_id)
        msg.attach(new_year)
        html = f.read().decode() %(image_id, html_footer)
    elif len(args) == 6:
        html = f.read().decode() % (idc_name, start_time, end_time, html_footer)
    f.close()

    msg_html_image = MIMEText(html, 'html', 'utf-8')
    msg.attach(msg_html_image)

    return msg


import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y%m%d %H:%M:%S"
logging.basicConfig(filename='send_mail.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def send_mail(msg):

    import smtplib
    mail_user = 'robot@51ywx.com'
    mail_pass = 'XbLKzpQ40bznIC7s'
    smtp_host = 'smtp.51ywx.com'
    smtp_port = 25
    smtp = smtplib.SMTP()
    # print(msg['Bcc'])
    if msg['Bcc']:
        receiver = msg['To'].split(',') + msg['Bcc'].split(',')
    else:
        receiver = msg['To'].split(',')
    # smtp.set_debuglevel(1)

    try:
        smtp.connect(smtp_host, smtp_port)
        smtp.login(mail_user, mail_pass)
        # 测试，发送开关
        # smtp.sendmail(msg['From'], receiver, msg.as_string())
        smtp.quit()
        log = 'Send mail to [ {0} ] successful!'.format(','.join(receiver))
        logging.info(log)
        print(log)
    except smtplib.SMTPConnectError as e:
        log = 'Send mail to [ {0} ] failed!'.format(','.join(receiver))
        logging.error(log)
        print('Send mail to ', ', '.join(receiver), ' successful!')
        print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        log = 'Send mail to [ {0} ] failed!'.format(','.join(receiver))
        logging.error(log)
        print('Send mail to ', ', '.join(receiver), ' successful!')
        print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        log = 'Send mail to [ {0} ] failed!'.format(','.join(receiver))
        logging.error(log)
        print('Send mail to ', ', '.join(receiver), ' successful!')
        print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        log = 'Send mail to [ {0} ] failed!'.format(','.join(receiver))
        logging.error(log)
        print('Send mail to ', ', '.join(receiver), ' successful!')
        print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPDataError as e:
        log = 'Send mail to [ {0} ] failed!'.format(','.join(receiver))
        logging.error(log)
        print('Send mail to ', ', '.join(receiver), ' successful!')
        print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        log = 'Send mail to [ {0} ] failed!'.format(','.join(receiver))
        logging.error(log)
        print('邮件发送失败, ', e.message)
    except Exception as e:
        log = 'Send mail to [ {0} ] failed!'.format(','.join(receiver))
        logging.error(log)
        print('邮件发送异常, ', str(e))


# 恭贺新春
# 在 get_mail_list_from_excel 中匹配 机房名称 与 客户名称 的时候，一定要手动处理，确保二者不能同时匹配上
subject = '【易网信】 恭贺新春'
image = "image/new_year_2019.png"
html = 'html_body_newYear.html'
# receiver = ['duoyichen@qq.com', 'duoyichen@163.com', 'pengmengya@51ywx.com']
# receiver = ['pengmengya@51ywx.com']
excel = '2019春节封网&祝福邮箱统计.xlsx'
receiver_list = get_mail_list_from_excel(excel)
for i in receiver_list:
    # print(len(i), ': ', i)
    # receiver_list 是一个二层
    for j in i:
        # print(type(j), j)
        receiver = j.split(',')
        msg = build_msg_html_image(subject, receiver, html, image)
        send_mail(msg)


# 封网通知
# 在 get_mail_list_from_excel 中匹配 机房名称 与 客户名称 的时候，一定要手动处理，确保二者不能同时匹配上
# excel = '机房.xlsx'
# excel = '2019春节封网&祝福邮箱统计.xlsx'
# subject = '【易网信】2019年春节封网通知'
# html = 'html_body_IDCNotify.html'
# idc_dic = get_mail_list_from_excel(excel)
# for k,v in idc_dic.items():
#     # print(k,':',)
#     for k2,v2 in v.items():
#         # print('    ',k2,': ',)
#         idc_name = v2['idc_name']
#         start_time = v2['start_time']
#         end_time = v2['end_time']
#         mail_list = v2['mail_list']
#         # print(mail_list)
#         receiver = mail_list.replace(' ','').split(',')
#         # print('        ', type(idc_name), idc_name)
#         # print('        ', type(start_time), start_time)
#         # print('        ', type(end_time), end_time)
#         # print('        ', type(receiver), receiver)
#         msg = build_msg_html_image(subject, receiver, html, start_time, end_time, idc_name)
#         send_mail(msg)































#构建文本邮件内容
# msg_text = MIMEText('自定义TEXT纯文本部分','plain','utf-8')
# msg.attach(msg_text)
#读取文件创建邮件内容
# with open('textfile','rb') as fp:   #读取文件内容
#     msg_text=MIMEText(fp.read(),'plain','utf-8')

#构建HTML格式的邮件内容
# msg_html = MIMEText("<h1>HTML格式邮件</h1>","html","utf-8")
# msg.attach(msg_html)
#构建HTML格式邮件带图片内容


#带附件的邮件MIMEApplication
# filename = '简历.pdf'
# with open(filename,'rb') as f:
#     attachfile = MIMEApplication(f.read())
# attachfile.add_header('Content-Disposition', 'attachment', filename=filename)
# msg.attach(attachfile)

#带多个附件的邮件MIMEApplication
# filenames = ['简历.pdf','副本.pdf']
# for tmp in filename:
#     with open(tmp,'rb') as f:
#         attachfiles = MIMEApplication(f.read())
#         attachfiles.add_header('Content-Disposition', 'attachment', filename=tmp)
#         msg.attach(attachfiles)

#带附件的邮件MIMEBase
# filename1 = '图片.pdf'
# attachfile_base = MIMEBase('application', 'octet-stream')  #创建基础对象指定类型
# attachfile_base.set_payload(open(filename,'rb').read())  #设置我有效负载
# attachfile_base.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', filename1) )
# encoders.encode_base64(attachfile_base)
# msg.attach(attachfile_base)

#创建音频文件
# AUDIO_HTML = '''
#     <p>this's audio file</p>
#     <audio controls>
#     <source src="cid:audioid" type="audio/mpeg">
#     </audio>
# '''
# msg_test1 = MIMEText(AUDIO_HTML,'html','utf-8')
# msg_audio = MIMEAudio(open('iphone.mp3','rb').read(),'plain')
# msg_audio.add_header('Content-ID','audioid')
# msg.attach(msg_test1)
# msg.attach(msg_audio)
#收到邮件不能播放，有待解决！