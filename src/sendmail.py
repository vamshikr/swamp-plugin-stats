import sys
import smtplib
from email.message import EmailMessage


def send(config, msg):

    subject = 'SWAMP plugin statistics'

    conn = smtplib.SMTP(host=config['host'], port=587)
    conn.starttls()
    conn.login(config['username'], config['password'])

    for address in config['to_address'].split(','):
        em = EmailMessage()
        em.set_content(msg)
        em['To'] = address
        em['From'] = config['username']
        em['Subject'] = subject
        conn.send_message(em)
    conn.quit()


if __name__ == '__main__':
    send(*sys.argv[1:])
