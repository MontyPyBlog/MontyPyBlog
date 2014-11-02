import os, sys

os.environ['APP_ENVIRONMENT'] = 'local'

os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''
os.environ['S3_BUCKET_NAME'] = ''
os.environ['S3_BUCKET_LOCATION'] = ''

# Unused for now
os.environ['DATABASE_HOST'] = ''
os.environ['DATABASE_USER'] = ''
os.environ['DATABASE_PASS'] = ''

#os.environ[''] = ''