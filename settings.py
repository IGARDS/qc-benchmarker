SECRET_KEY = 'not_a_secret'
CELERY_BROKER_URL='redis://localhost:6379/0'
CELERY_RESULT_BACKEND='redis://localhost:6379/0'

OUTPUT_DIR = "/data/files"
if OUTPUT_DIR[-1] != "/":
    OUTPUT_DIR = OUTPUT_DIR+"/"
    
FILES_TO_RENDER = ["master.Rmd","full_report.Rmd","sample.Rmd","lc.Rmd","source.Rmd","ms1.Rmd","ms2.Rmd"] # These are processed in order

BASIC_AUTH_USERNAME = 'qc'
BASIC_AUTH_PASSWORD = 'thiswaseasy'

BASIC_AUTH_FORCE = True