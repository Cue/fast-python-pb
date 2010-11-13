from distutils.core import setup, Extension
setup(name="{{ moduleName }}", version="1.0",
      ext_modules=[
        {% for name in files %}
          Extension("{{ name }}", ["{{ name }}.c"], libraries=['protobuf']),
        {% endfor %}
      ])
