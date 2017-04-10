from twisted.enterprise import adbapi
from boto.sqs.message import RawMessage
import datetime
import boto.sqs
import json
import logging
import os

logger = logging.getLogger(__name__)

conf = {
	"sqs-access-key": os.getenv('ASYNCRO_AWS_KEY', ""),
	"sqs-secret-key": os.getenv('ASYNCRO_AWS_SECRET', ""),
	"sqs-queue-name": "gplay-app-details",
	"sqs-region": os.getenv('ASYNCRO_AWS_REGION', "")
}

class SQSStorePipeline(object):

    def __init__(self):
        self.sqs = conn = boto.sqs.connect_to_region(
            conf.get('sqs-region'),
            aws_access_key_id = conf.get('sqs-access-key'),
            aws_secret_access_key = conf.get('sqs-secret-key')
        )
        self.queue = self.sqs.get_queue(conf.get('sqs-queue-name'))

    def process_item(self, item, spider):
        # run db query in thread pool
        logger.debug('process item----------------------')
        m = RawMessage()
        m.set_body(json.dumps(item))
        retval = self.queue.write(m)
        logger.debug('added message, got retval: %s' % retval)

        return item

    def safeValue(self,value):
        if value == [] :
            return ''
        else :
            return value[0].encode("utf-8")

    def handle_error(self, e):
        logger.error(e)