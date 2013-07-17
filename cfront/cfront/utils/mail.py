import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'crispr.scan@gmail.com'
SMTP_PASSWORD = 'crisprpassword'


def mail_new_job(request, job):
    subject = "Job Submission to CRISPR.mit.edu"
    msg_tmp = """You've successfully submitted a job -- ({job_name}) to the CRISPR/guides selection server at crispr.mit.edu. To see its output, you can head over to {host}/job/{job_id} where results from the offtarget scan will be reported as they come in."""
    message = msg_tmp.format(email=job.email, job_name=job.name, job_id = job.id, host=request.host)
    send_mail(job.email, subject, message)

def send_mail(email_address, subject, message):
    #restrict_domain = pb_settings['email.restrict_domain']
    #if restrict_domain and not email_address.endswith('@pictobin.com'):
    #    email_debug(email_address, subject, message)
    #    return
    email = MIMEMultipart()
    email['From'] = SMTP_USER
    email['To'] = email_address
    email['Subject'] = subject
    email.attach(MIMEText(message))
    mailServer = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(SMTP_USER, SMTP_PASSWORD)
    mailServer.sendmail(SMTP_USER, email_address, email.as_string())
    mailServer.close()
