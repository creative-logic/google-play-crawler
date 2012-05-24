from twisted.enterprise import adbapi
import datetime
import MySQLdb.cursors

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
