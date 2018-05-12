import urllib.request
import urllib.parse
import ssl  
import smtplib
import time
from email.mime.text import MIMEText



# This restores the same behavior as before.  
context = ssl._create_unverified_context()  


bookname = input('请输入小说名字')
startcharpter = input('请输入开始章节名称')
pages = input('要看几章')
booknameurl = urllib.parse.quote(bookname)
url = 'https://www.biquge5200.com/modules/article/search.php?searchkey='+str(booknameurl)


def sent_mail(subject,content):
    msg_from='*****'                                #发送方邮箱
    passwd='********'                                  #填入发送方邮箱的授权码
    msg_to='*****'                                 #收件人邮箱
                            
                                        #主题     
        #正文
    msg = MIMEText(content)
    msg['Subject'] = subject +'from python'
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print ('发送成功!    '+subject)
    except s.SMTPExceptione:
        print ("发送失败")
    finally:
        s.quit()

def find_firstcharpter(muluurl):#find the first charpter
    mulu = urllib.request.urlopen(muluurl,context=context)
    mulu = mulu.read().decode('gbk')
    starta = mulu.find('正文')
    firstb = mulu.find(startcharpter,starta)-2
    firsta = mulu.find('<a href=',firstb-100) + 9
    return mulu[firsta:firstb]

def find_book(bookname,url): #find the book url
    search = urllib.request.urlopen(url,context=context)
    html = search.read().decode('gbk')
    mulub = html.find(bookname)-2
    mulua = html.find('<a href=',mulub-100) + 9
    return html[mulua:mulub]

def find_content(charpterurl):#find the content
    zhengwen = urllib.request.urlopen(charpterurl,context=context)
    zhengwen =zhengwen.read().decode('gbk')
    zhengwen=zhengwen.replace('<br/>','\n')
    x = zhengwen.find('<div id="content">')+len('<div id="content">')
    y = zhengwen.find('</div>',x+10)
    content=(zhengwen[x:y])
    t1 = zhengwen.find('<h1>')+4
    t2 = zhengwen.find('</h1>')
    subject = bookname+zhengwen[t1:t2]
    n2 = zhengwen.find('下一章')-2
    n1 = zhengwen.find('<a href=',n2-100)+len('<a href="')
    nextpageurl = zhengwen[n1:n2]
    return (content,subject,nextpageurl)
    


def booksearch(bookname):
    muluurl = find_book(bookname,url)
    charpterurl = find_firstcharpter(muluurl)
    (content,subject,nextpageurl) = find_content(charpterurl)
    a=1
    while a<=int(pages) :
        sent_mail(subject,content)
        (content,subject,nextpageurl)=find_content(nextpageurl)
        time.sleep(5)
        a+=1
    else :
        print('好啦~发送完毕啦')
    

if __name__ == '__main__':
    booksearch(bookname)
    
