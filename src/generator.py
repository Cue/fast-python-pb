from jinja2 import Environment, FileSystemLoader

import os.path
import tempfile

def main():
  path = tempfile.mkdtemp()
  cFilePath = os.path.join(path, 'sample.c')
  setupPyPath = os.path.join(path, 'setup.py')

  context = {
    'moduleName': 'sample',
    'className': 'Woot',
    'members': [
      {'name': 'this'},
      {'name': 'thing'}
    ]
  }

  templatePath = os.path.join(os.path.dirname(__file__), '../template')
  templateEnv = Environment(loader=FileSystemLoader(templatePath))
  with open(cFilePath, 'w') as f:
    f.write(templateEnv.get_template('module.jinja.c').render(context))
  with open(setupPyPath, 'w') as f:
    f.write(templateEnv.get_template('setup.jinja.py').render(context))
  print path

if __name__ == '__main__':
  main()
