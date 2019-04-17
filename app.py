from __future__ import absolute_import
from os import path, environ
import json
from flask import Flask, Blueprint, abort, jsonify, request, session, send_from_directory, url_for
import settings
from celery import Celery
import urllib.parse
import logging
import os
import sys as sys2

from flask import render_template, Blueprint, request, make_response
from werkzeug.utils import secure_filename

import tempfile

import subprocess

import glob

#from pydrop import config

#blueprint = Blueprint('templated', __name__, template_folder='templates')

log = logging.getLogger('pydrop')

app = Flask(__name__)
app.config.from_object(settings)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

output_dir = "/tmp"
if output_dir[-1] != "/":
    output_dir = output_dir+"/"

def glob_ctime_sort(path):
    files = glob.glob(path)
    files.sort(key=os.path.getctime)
    return files

def get_url(task_id):
    print(task_id)
    try:
        file = preprocess_task.AsyncResult(task_id).get(timeout=1.0)
    except:
        return "RUNNING"
    
    return url_for('view_results',path=urllib.parse.quote(file, safe=''))

@app.route('/index/')
@app.route('/index/<work_dir>')
def index(work_dir=None):
    if work_dir == None:
        # Route to serve the upload form
        work_dir = tempfile.mkdtemp(prefix="qc_benchmarker_",dir=output_dir).replace(output_dir,"")
    raw_files = [file.split('/')[-1].replace(".raw","") for file in glob_ctime_sort("%s%s/*.raw"%(output_dir,work_dir))]
    result_files = glob_ctime_sort("%s%s/*.result"%(output_dir,work_dir))
    valid_result_files = {}
    for i,result_file in enumerate(result_files):
        try:
            context = json.loads(open(result_file).read())
        except:
            print("Invalid json in %s"%result_file)
            continue
        if "method" in context:
            print(get_url(context["id"]))
            valid_result_files[context["method"]] = get_url(context["id"])
    return render_template('index.html',
                           page_name='QC Benchmarker',
                           project_name="qc-benchmarker",
                           work_dir=work_dir,
                           raw_files=raw_files,
                           result_files=valid_result_files
                          )

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    work_dir = request.form["work_dir"]

    save_path = os.path.join(work_dir, secure_filename(file.filename))
    current_chunk = int(request.form['dzchunkindex'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
        return make_response(('File already exists', 400))

    try:
        with open(save_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())
    except OSError:
        # log.exception will include the traceback so we can see what's wrong 
        log.exception('Could not write to file')
        return make_response(("Not sure why,"
                              " but we couldn't write the file to disk", 500))

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
            log.error(f"File {file.filename} was completed, "
                      f"but has a size mismatch."
                      f"Was {os.path.getsize(save_path)} but we"
                      f" expected {request.form['dztotalfilesize']} ")
            return make_response(('Size mismatch', 500))
        else:
            log.info(f'File {file.filename} has been uploaded successfully')
    else:
        log.debug(f'Chunk {current_chunk + 1} of {total_chunks} '
                  f'for file {file.filename} complete')

    return make_response(("Chunk upload successful", 200))

@celery.task(name="tasks.preprocess")
def preprocess_task(output_dir,work_dir,raw_file):
    output_file = raw_file + ".html"
    output_dir = "%s%s/%s"%(output_dir,work_dir,preprocess_task.request.id)
    os.mkdir(output_dir)
    try:
        cmd = "cd %s; R -e 'QUERY=\"%s\"; rmarkdown::render(\"/data/qc-benchmarker/preprocess.Rmd\",output_dir=\"%s\",output_file=\"%s\")'"%(output_dir,raw_file,output_dir,output_file)
        subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT)
    except:
        print("Error while running: %s"%cmd)
    file = "%s/%s"%(output_dir,output_file)
    print(file)
    return file

@app.route("/run/<method>/<raw_file>", methods=['POST'])
def run(method,raw_file):
    content = request.json
    work_dir = content["work_dir"]
    #raw_file = output_dir + work_dir + "/" + raw_file+".raw"
    if method == "preprocess":
        res = preprocess_task.delay(output_dir,work_dir,raw_file)
    context = {"id": res.task_id, "method": method, "raw_file": raw_file}
    open("%s%s/%s.result"%(output_dir,work_dir,res.task_id),"w").write(json.dumps(context, indent=4))
    return jsonify(context)

@app.route('/view_results/<path>')
def view_results(path):
    path=urllib.parse.unquote(path)
    work_dir = "/".join(path.split("/")[0:-1])
    file_name = path.split("/")[-1]  
    return send_from_directory(work_dir,file_name)



if __name__ == "__main__":
    port = int(environ.get("PORT", 7777))
    app.run(host='0.0.0.0', port=port, debug=True)
