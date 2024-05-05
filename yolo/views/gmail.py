# Mail
# from smtplib import SMTP
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 상수 선언
# smtp 서버와 연결
GMAIL_SMTP = "smtp.gmail.com"
GMAIL_PORT = 465

# 로그인
MY_ACCOUNT = "71goodhabits@gmail.com"
# MY_PASSWORD = "dy't^svNd"
MY_PASSWORD = "aqlq biej scue ggob" # GMail 앱비밀번호

# 메일받을 계정
# RECEIVE_ACCOUNT = "7goodhabit@naver.com"

def sendEmail(RECEIVE_ACCOUNT, msg):
    # smtp 서버와 연결
    smtp = smtplib.SMTP_SSL(GMAIL_SMTP, GMAIL_PORT)
    
    # 로그인
    smtp.login(MY_ACCOUNT, MY_PASSWORD)
    
    # 유효성 체크
    reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]{2,3}$"
    
    if re.match(reg, RECEIVE_ACCOUNT):
        smtp.sendmail(MY_ACCOUNT, RECEIVE_ACCOUNT, msg.as_string())
        print("정상적으로 메일이 발송되었습니다.")
    else:
        print("받으실 메일주소를 정확히 입력하세요.")

    # smtp 서버 연결 해제
    smtp.quit() 
    
def writeEmail(receive_account, mail_title, mail_content, predicted_image):
    
    # 메일 기본정보 설정
    msg = MIMEMultipart()
    msg["Subject"] = mail_title
    msg["From"] = MY_ACCOUNT
    msg["To"] = receive_account
    
    # 메일 본문내용
    content = mail_content
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)
    
    # 이미지파일 추가
    image_name = predicted_image
    with open(image_name, 'rb') as file:
        img = MIMEImage(file.read())
        img.add_header('Content-Disposition', 'attachment', filename=image_name)
        msg.attach(img)
    
    # 받는메일 유효성 검사 거친후 메일 전송
    sendEmail(receive_account, msg)
