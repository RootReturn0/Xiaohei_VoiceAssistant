import poplib
import os
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from threading import Timer
import time

import speak_api

email = '2175997289@qq.com'
passwd = 'tdvfmrszccwtdjcb'
pop_server = 'pop.qq.com'

def server_mail():
    server = poplib.POP3_SSL(pop_server, '995')
    print(server.getwelcome().decode('utf-8'))
    server.user(email)
    server.pass_(passwd)
    resp, mails, octets = server.list()
    first_index = len(mails)
    server.quit()
    watch_mail(first_index)


def watch_mail(first_index):
    server = poplib.POP3_SSL(pop_server, '995')
    # print(server.getwelcome().decode('utf-8'))
    server.user(email)
    server.pass_(passwd)

    # 返回所有邮件编号
    resp, mails, octets = server.list()
    index = len(mails)
    # print(index)
    if first_index==index:
        # print("no email")
        server.quit()
        t=Timer(20,watch_mail(first_index))
        t.start()
        print("watch_email",len(mails));
    else:
        print("new email!",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        path = "./resource/reminder.wav"
        os.system('play ' + path)
        resp, lines, octets = server.retr(index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')

        # 把邮件内容解析为Massage对象，用来解析邮件
        msg = Parser().parsestr(msg_content)
        res = print_info(msg)
        #这里是邮件的全部内容👇
        speak_api.say("您有一封新邮件:"+res)

        server.quit()
        t = Timer(20, watch_mail(index))
        t.start()


# 解析邮件内容
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value,charset=decode_header(s)[0]
    if charset:
        value=value.decode(charset)
        return value
    else:
        return value


def print_info(msg, indent=0):
    email_content=''
    email_content_header = ''
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % ('  ' * indent, header, value))
            if header=='From':
                # sender=value[value.rfind('<')+1:value.rfind('>')]
                sender = value[0:value.rfind('<')-1]
                email_content_header+='您收到一封来自'+sender+'的邮件。'
            elif header=='Subject':
                email_content_header+='主题为'+(str)(value)+'。'
        # print("email_content_header", email_content)
        
    email_content+=email_content_header

    parts = msg.get_payload()
    for n, part in enumerate(parts[:len(parts) - 1]):
        content_type = part.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = part.get_payload(decode=True)
            charset = guess_charset(part)
            if charset:
                content = content.decode(charset)
            content=content.replace('&nbsp;', '')
            content = content.replace(' ', '')
            content = content.replace('\n', '')
            content = content.replace('\r', '')
            # print('%sText: %s' % ('  ' * indent, content + '...'))
            email_content=email_content+'邮件内容：'+content
        else:
            print('%附件: %s' % ('  ' * indent, content_type))
    return  email_content

if __name__ == '__main__':
    server_mail()
