import logging 
from logging import handlers


HOST = ("mailo2.uhc.com",25)
FROM = "parkinson-tracker@optum.com"
TO = 'jelo_salomon@optum.com'
SUBJECT = 'DETERIORATION'

# Setup logging
logging.basicConfig(level = logging.INFO)
handler = handlers.SMTPHandler(HOST, FROM, TO, SUBJECT)

email_logger = logging.getLogger('smtp.example')
email_logger.addHandler(handler)
email_logger.setLevel = logging.INFO

logging.info('TEST EMAIL')
logging.shutdown()