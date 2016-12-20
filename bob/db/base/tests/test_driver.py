import tempfile
import shutil
import os

from ..driver import download

if 'DOCSERVER' in os.environ:
  USE_SERVER=os.environ['DOCSERVER']
else:
  USE_SERVER='https://www.idiap.ch'

class Namespace(object):
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)


def test_download_01():
  tmpdir = tempfile.mkdtemp()
  try:
    arguments = Namespace(files=[tmpdir+'/db.sql3'], force=False,
        name='does_not_exist', test_dir=tmpdir, version='0.9.0',
        source='%s/software/bob/databases/latest/' % USE_SERVER)
    assert download(arguments) == 1 #error #error #error #error
    arguments = Namespace(files=[tmpdir+'/db.sql3'], force=False,
        name='banca', test_dir=tmpdir, version='0.9.0',
        source='%s/software/bob/databases/latest/' % USE_SERVER)
    assert download(arguments) == 0 #success
  finally:
    shutil.rmtree(tmpdir)
