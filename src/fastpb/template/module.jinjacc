#include <Python.h>
#include "structmember.h"
#include "{{ moduleName }}.pb.h"

{% for message in messages %}
  typedef struct {
      PyObject_HEAD
      {% for member in message.field %}
        PyObject *{{ member.name }};
      {% endfor %}

      {{ package }}::{{ message.name }} protobuf;
  } {{ message.name }};

  static void
  {{ message.name }}_dealloc({{ message.name }}* self)
  {
      {% for member in members %}
        Py_XDECREF(self->{{ member.name }});
      {% endfor %}
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
      return 0;
  }


  {% for member in message.field %}
    static PyObject *
    {{ message.name }}_get{{ member.name }}({{ message.name }} *self, void *closure)
    {
        Py_INCREF(self->{{ member.name }});
        return self->{{ member.name }};
    }

    static int
    {{ message.name }}_set{{ member.name }}({{ message.name }} *self, PyObject *value, void *closure)
    {
      if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the {{ member.name }} attribute");
        return -1;
      }

      if (! PyString_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The {{ member.name }} attribute value must be a string");
        return -1;
      }

      Py_DECREF(self->{{ member.name }});
      Py_INCREF(value);
      self->{{ member.name }} = value;

      return 0;
    }
  {% endfor %}


  static PyMemberDef {{ message.name }}_members[] = {
      {NULL}  /* Sentinel */
  };


  static PyGetSetDef {{ message.name }}_getsetters[] = {
    {% for member in message.field %}
      {(char *)"{{ member.name }}",
       (getter){{ message.name }}_get{{ member.name }}, (setter){{ message.name }}_set{{ member.name }},
       (char *)"",
       NULL},
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
      "{{ message.name }} objects",        /* tp_doc */
      0,                                   /* tp_traverse */
      0,                                   /* tp_clear */
      0,                		               /* tp_richcompare */
      0,		                               /* tp_weaklistoffset */
      0,                		               /* tp_iter */
      0,		                               /* tp_iternext */
      {{ message.name }}_methods,          /* tp_methods */
      {{ message.name }}_members,          /* tp_members */
      {{ message.name }}_getsetters,       /* tp_getset */
      0,                                   /* tp_base */
      0,                                   /* tp_dict */
      0,                                   /* tp_descr_get */
      0,                                   /* tp_descr_set */
      0,                                   /* tp_dictoffset */
      (initproc){{ message.name }}_init,   /* tp_init */
      0,                                   /* tp_alloc */
      {{ message.name }}_new,              /* tp_new */
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