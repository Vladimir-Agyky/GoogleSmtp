from flask import Flask, jsonify

import imaplib
import email
from email.header import decode_header

app = Flask(__name__)

# IMAP 서버 연결
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
# 로그인
imap_server.login('id', 'pw')

# INBOX에서 이메일 가져오기
imap_server.select('INBOX')

# 모든 이메일 검색
status, messages = imap_server.search(None, 'ALL', '1:10')
emails = []

if status == 'OK':
    for num in messages[0].split():
        # 이메일 가져오기
        status, message = imap_server.fetch(num, '(RFC822)')
        if status == 'OK':
            # 이메일 파싱
            email_message = email.message_from_bytes(message[0][1])
            subject = decode_header(email_message['Subject'])[0][0]
            if isinstance(subject, bytes):
                # 인코딩이 있다면 디코딩
                subject = subject.decode()
            sender = email_message['From']
            sender = decode_header(sender)[0][0]
            if isinstance(sender, bytes):
                sender = sender.decode()
            email_data = {'subject': subject, 'from': sender}
            emails.append(email_data)

# 연결 종료
imap_server.close()
imap_server.logout()

#print(emails)
#print(jsonify(emails))

cnt = 1
for email in emails:
    print(f'{cnt} : {email}')
    cnt += 1