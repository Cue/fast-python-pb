#include <Python.h>
#include "structmember.h"

{% for message in messages %}
  typedef struct {
      PyObject_HEAD
      {% for member in message.field %}
        PyObject *{{ member.name }};
      {% endfor %}
  } {{ message.name }};

  static int
  {{ message.name }}_traverse({{ message.name }} *self, visitproc visit, void *arg)
  {
    {% for member in message.field %}
      Py_VISIT(self->{{ member.name }});
    {% endfor %}
      return 0;
  }

  static int
  {{ message.name }}_clear({{ message.name }} *self)
  {
    {% for member in message.field %}
      Py_CLEAR(self->{{ member.name }});
    {% endfor %}
      return 0;
  }

  static void
  {{ message.name }}_dealloc({{ message.name }}* self)
  {
      {{ message.name }}_clear(self);
      self->ob_type->tp_free((PyObject*)self);
  }

  static PyObject *
  {{ message.name }}_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
  {
      {{ message.name }} *self;

      self = ({{ message.name }} *)type->tp_alloc(type, 0);
      if (self != NULL) {
        {% for member in message.field %}
          self->{{ member.name }} = Py_None;
        {% endfor %}
      }

      return (PyObject *)self;
  }

  static int
  {{ message.name }}_init({{ message.name }} *self, PyObject *args, PyObject *kwds)
  {
    {% for member in message.field %}
      PyObject *{{ member.name }}=NULL;
    {% endfor %}
      PyObject *tmp;

      static char *kwlist[] = {
        {% for member in message.field %}
          "{{ member.name }}",
        {% endfor %}
        NULL
      };

      if (! PyArg_ParseTupleAndKeywords(
          args, kwds, "|OO", kwlist,
          {% for member in message.field %}
            &{{ member.name }}
            {% if not loop.last %}
              ,
            {% endif %}
          {% endfor %}
          ))
          return -1;

    {% for member in message.field %}
      if ({{ member.name }}) {
          tmp = self->{{ member.name }};
          Py_INCREF({{ member.name }});
          self->{{ member.name }} = {{ member.name }};
          if (tmp) {
            Py_XDECREF(tmp);
          }
      }
    {% endfor %}

      return 0;
  }


  static PyMemberDef {{ message.name }}_members[] = {
    {% for member in message.field %}
      {"{{ member.name }}", T_OBJECT_EX, offsetof({{ message.name }}, {{ member.name }}), 0,
       "{{ member.description }}"},
    {% endfor %}
      {NULL}  /* Sentinel */
  };

  static PyMethodDef {{ message.name }}_methods[] = {
      {NULL}  /* Sentinel */
  };

  static PyTypeObject {{ message.name }}Type = {
      PyObject_HEAD_INIT(NULL)
      0,                                   /*ob_size*/
      "{{ moduleName }}.{{ message.name }}",  /*tp_name*/
      sizeof({{ message.name }}),             /*tp_basicsize*/
      0,                                   /*tp_itemsize*/
      (destructor){{ message.name }}_dealloc, /*tp_dealloc*/
      0,                                   /*tp_print*/
      0,                                   /*tp_getattr*/
      0,                                   /*tp_setattr*/
      0,                                   /*tp_compare*/
      0,                                   /*tp_repr*/
      0,                                   /*tp_as_number*/
      0,                                   /*tp_as_sequence*/
      0,                                   /*tp_as_mapping*/
      0,                                   /*tp_hash */
      0,                                   /*tp_call*/
      0,                                   /*tp_str*/
      0,                                   /*tp_getattro*/
      0,                                   /*tp_setattro*/
      0,                                   /*tp_as_buffer*/
      Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC, /*tp_flags*/
      "{{ message.name }} objects",           /* tp_doc */
      (traverseproc){{ message.name }}_traverse,   /* tp_traverse */
      (inquiry){{ message.name }}_clear,           /* tp_clear */
      0,		               /* tp_richcompare */
      0,		               /* tp_weaklistoffset */
      0,		               /* tp_iter */
      0,		               /* tp_iternext */
      {{ message.name }}_methods,             /* tp_methods */
      {{ message.name }}_members,             /* tp_members */
      0,                         /* tp_getset */
      0,                         /* tp_base */
      0,                         /* tp_dict */
      0,                         /* tp_descr_get */
      0,                         /* tp_descr_set */
      0,                         /* tp_dictoffset */
      (initproc){{ message.name }}_init,      /* tp_init */
      0,                         /* tp_alloc */
      {{ message.name }}_new,                 /* tp_new */
  };

{% endfor %}

static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
init{{ moduleName }}(void)
{
    PyObject* m;

    {% for message in messages %}
      if (PyType_Ready(&{{ message.name }}Type) < 0)
          return;
    {% endfor %}

    m = Py_InitModule3("{{ moduleName }}", module_methods,
                       "{{ moduleDescription }}");

    if (m == NULL)
      return;

    {% for message in messages %}
      Py_INCREF(&{{ message.name }}Type);
      PyModule_AddObject(m, "{{ message.name }}", (PyObject *)&{{ message.name }}Type);
    {% endfor %}
}