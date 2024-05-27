import smtplib
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('saurabh544321@gmail.com' , 'toot jqsg pdhe fadh')
server.sendmail("saurabh544321@gmail.com","lohanidivya290@gmail.com","this is from python")
print("mail send")