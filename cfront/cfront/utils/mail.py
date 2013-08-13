import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

from smtplib import SMTPAuthenticationError

#SMTP_SERVER = 'smtp.gmail.com'
#SMTP_PORT = 587
SMTP_USER = 'scan@crispr.mit.edu'
#SMTP_PASSWORD = 'crisprpassword'


def mail_new_job(request, job):
    subject = "Job Submission to CRISPR.mit.edu"
    msg_tmp = """You've successfully submitted a job -- ({job_name}) to the CRISPR/guides selection server at crispr.mit.edu. To see its output, you can head over to {host}/job/{job_key} where results from the offtarget scan will be reported as they come in."""
    message = msg_tmp.format(email=job.email, job_name=job.name, job_key = job.key, host=request.host)
    send_mail(job.email, subject, message)

def mail_completed_job(request, job):
    subject = "Job Completed at CRISPR.mit.edu"
    msg_tmp = """Your recent job -- ({job_name}) has run to completion at crispr.mit.edu. To see its output, please head over to http://crispr.mit.edu/job/{job_key}."""
    message = msg_tmp.format(email=job.email, job_name=job.name, job_key = job.key )
    send_mail(job.email, subject, message)

def send_mail(email_address, subject, message):
    #restrict_domain = pb_settings['email.restrict_domain']
    #if restrict_domain and not email_address.endswith('@pictobin.com'):
    #    email_debug(email_address, subject, message)
    #    return

    try: 

        email = MIMEMultipart()
        email['From'] = SMTP_USER
        email['To'] = email_address
        email['Subject'] = subject
        email.attach(MIMEText(message))

        server = smtplib.SMTP('localhost')
        server.set_debuglevel(1)
        server.sendmail(SMTP_USER,email_address, email.as_string())
        server.quit()

    except SMTPAuthenticationError as e:
        print "failed to send mail due to error"
        print e
