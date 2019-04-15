from __future__ import absolute_import
from os import path, environ
import json
from flask import Flask, Blueprint, abort, jsonify, request, session
import settings
from celery import Celery

import logging
import os

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

@app.route('/<work_dir>')
@app.route('/index/<work_dir>')
def index(work_dir):
    if work_dir == None:
        # Route to serve the upload form
        work_dir = tempfile.mkdtemp(prefix="qc_benchmarker_",dir=output_dir)
    if output_dir not in work_dir:
        work_dir = output_dir+"/"+work_dir
    raw_files = [file.split('/')[-1] for file in glob.glob("%s/*.raw"%work_dir)]
    mzML_files = [file.split('/')[-1] for file in glob.glob("%s/*.mzML"%work_dir)]
    result_files = []
    for result_file in glob.glob("%s/*.result"%work_dir):
        result_files.append(tuple(open(result_file).read().split("\t")))
    return render_template('index.html',
                           page_name='QC Benchmarker',
                           project_name="qc-benchmarker",
                           work_dir=work_dir,
                           raw_files=raw_files,
                           result_files=result_files
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

@celery.task(name="tasks.qc_preprocess")
def qc_preprocess_task(raw_files):
    results = []
    for raw_file in raw_files:
        work_dir = "/".join(raw_file.split("/")[0:-1])
        output_dir = "%s/%s"%(work_dir,qc_preprocess_task.request.id)
        #try:
        os.mkdir(output_dir)
        #except:
        #    pass
        results.append(str(subprocess.check_output("cd %s; R -e 'QUERY=\"%s\"; rmarkdown::render(\"/data/qc-benchmarker/preprocess.Rmd\",output_dir=\"%s\")'"%(work_dir,raw_file,output_dir),shell=True)))
    return repr(results)

@app.route("/qc_preprocess", methods=['POST'])
def qc_preprocess():
    content = request.json
    work_dir = content["work_dir"]
    raw_files = glob.glob("%s/*.raw"%work_dir)
    res = qc_preprocess_task.delay(raw_files)
    open("%s/%s.result"%(work_dir,res.task_id),"w").write("qc_preprocess(%s)"%str(raw_files)+"\t/qc_preprocess/result/"+str(res.task_id))
    context = {"id": res.task_id, "work_dir": work_dir}
    return jsonify(context)

@app.route("/qc_preprocess/result/<task_id>")
def qc_preprocess_result(task_id):
    retval = qc_preprocess_task.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)

if __name__ == "__main__":
    port = int(environ.get("PORT", 7777))
    app.run(host='0.0.0.0', port=port, debug=True)
