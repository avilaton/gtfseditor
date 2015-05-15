import sys
import boto
import boto.s3
from boto.s3.key import Key

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3(object):
	"""S3 Service"""

	def __init__(self, bucket_name):
		self.bucket_name = bucket_name

	def config(self, config):
		self.conn = boto.connect_s3(config['AWS_ACCESS_KEY_ID'],
			config['AWS_SECRET_ACCESS_KEY'],
			host="s3-us-west-1.amazonaws.com")

	def uploadFile(self, filename):
		bucket = self.conn.get_bucket(self.bucket_name)
		k = bucket.new_key(filename)
		k.set_contents_from_filename(filename, policy='public-read')

	def uploadFileObj(self, filename, fileObj):
		logger.info('Uploading {0} to Amazon S3 bucket {1}'.format(filename,
			self.bucket_name))
		bucket = self.conn.get_bucket(self.bucket_name)
		k = bucket.new_key(filename)
		k.set_contents_from_string(fileObj.getvalue(), policy='public-read')

	def ls(self):
		bucket = self.conn.get_bucket(self.bucket_name)
		return bucket.list()

	def mkbucket(self, bucket_name):
		return self.conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

def main(uploadfile):
	BUCKET_NAME = 'gtfseditor-feeds'
	s3service = S3(BUCKET_NAME)

	print 'Uploading %s to Amazon S3 bucket %s' % \
		(uploadfile, BUCKET_NAME)

	s3service.upload(uploadfile)

if __name__ == '__main__':

	main(sys.argv[1])