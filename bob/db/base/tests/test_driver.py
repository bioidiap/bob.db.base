import tempfile
import shutil

from ..driver import download


class Namespace(object):
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)




def test_download_01():
  tmpdir = tempfile.mkdtemp()
  try:
    arguments = Namespace(files=[tmpdir+'/db.sql3'], force=False, name='non_existing_db', source='http://www.idiap.ch/software/bob/databases/latest/', type='sqlite', version='0.9.0')
    assert download(arguments) == True
    arguments = Namespace(files=[tmpdir+'/db.sql3'], force=False, name='biowave_test', source='http://www.idiap.ch/software/bob/databases/latest/', type='sqlite', version='0.9.0')
    assert download(arguments) == False  
  finally:
    shutil.rmtree(tmpdir)


