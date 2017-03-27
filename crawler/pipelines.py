from twisted.enterprise import adbapi
import datetime
import MySQLdb.cursors
import boto.sqs
from boto.sqs.message import RawMessage
import json

conf = {
	"sqs-access-key": "",
	"sqs-secret-key": "",
	"sqs-queue-name": "",
	"sqs-region": "us-east-1",
	"sqs-path": "sqssend"
}

class SQSStorePipeline(object):

    def __init__(self):
	    self.sqs = conn = boto.sqs.connect_to_region(
	        conf.get('sqs-region'),
	        aws_access_key_id = conf.get('sqs-access-key'),
	        aws_secret_access_key = conf.get('sqs-secret-key')
		)
		self.queue = self.sqs.get_queue(conf.get('end-queue'))

    def process_item(self, item, spider):
        # run db query in thread pool
        print 'process item----------------------'
        m = RawMessage()
		m.set_body(json.dumps(item))
		retval = self.queue.write(m)
		print 'added message, got retval: %s' % retval

        return item

    def safeValue(self,value):
        if value == [] :
            return ''
        else :
            return value[0].encode("utf-8")

    def handle_error(self, e):
        print e

class SQLStorePipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='bam', user='root', passwd='passw0rd', cursorclass=MySQLdb.cursors.DictCursor, charset='utf8', use_unicode=True)
        #pass

    def process_item(self, item, spider):
        # run db query in thread pool
        print 'process item----------------------'
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        tx.execute("select name from application where name = %s", (self.safeValue(item['name']), ))
        result = tx.fetchone()
        if result:
            print 'exist --- ' + self.safeValue(item['name'])
        else:
            tx.execute(\
                "insert into application (name , author , rating,votes,image,fileSize,datePublished,contentRating,category,price,downloads,description,screenShots,version) values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (self.safeValue(item['name']),self.safeValue(item['author']),self.safeValue(item['rating']),self.safeValue(item['votes']),self.safeValue(item['image']),self.safeValue(item['fileSize']),self.safeValue(item['datePublished']),self.safeValue(item['contentRating']),self.safeValue(item['category']),self.safeValue(item['price']),self.safeValue(item['downloads']),self.safeValue(item['description']),item['screenShots'].encode("utf-8"),self.safeValue(item['version']))
            )
            print 'store --------'

    def safeValue(self,value):
        if value == [] :
            return ''
        else :
            return value[0].encode("utf-8")

    def handle_error(self, e):
        print e