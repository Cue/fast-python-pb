from distutils.core import setup, Extension
setup(name="{{ moduleName }}", version="1.0",
      ext_modules=[Extension("{{ moduleName }}", ["{{ moduleName }}.c"])])
