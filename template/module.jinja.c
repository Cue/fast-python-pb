#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    {% for member in members %}
      PyObject *{{ member.name }};
    {% endfor %}
} {{ className }};

static int
{{ className }}_traverse({{ className }} *self, visitproc visit, void *arg)
{
  {% for member in members %}
    Py_VISIT(self->{{ member.name }});
  {% endfor %}
    return 0;
}

static int
{{ className }}_clear({{ className }} *self)
{
  {% for member in members %}
    Py_CLEAR(self->{{ member.name }});
  {% endfor %}
    return 0;
}

static void
{{ className }}_dealloc({{ className }}* self)
{
    {{ className }}_clear(self);
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
{{ className }}_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    {{ className }} *self;

    self = ({{ className }} *)type->tp_alloc(type, 0);
    if (self != NULL) {
      {% for member in members %}
        self->{{ member.name }} = Py_None;
      {% endfor %}
    }

    return (PyObject *)self;
}

static int
{{ className }}_init({{ className }} *self, PyObject *args, PyObject *kwds)
{
  {% for member in members %}
    PyObject *{{ member.name }}=NULL;
  {% endfor %}
    PyObject *tmp;

    static char *kwlist[] = {
      {% for member in members %}
        "{{ member.name }}",
      {% endfor %}
      NULL
    };

    if (! PyArg_ParseTupleAndKeywords(
        args, kwds, "|OO", kwlist,
        {% for member in members %}
          &{{ member.name }}
          {% if not loop.last %}
            ,
          {% endif %}
        {% endfor %}
        ))
        return -1;

  {% for member in members %}
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


static PyMemberDef {{ className }}_members[] = {
  {% for member in members %}
    {"{{ member.name }}", T_OBJECT_EX, offsetof({{ className }}, {{ member.name }}), 0,
     "{{ member.description }}"},
  {% endfor %}
    {NULL}  /* Sentinel */
};

static PyMethodDef {{ className }}_methods[] = {
    {NULL}  /* Sentinel */
};

static PyTypeObject {{ className }}Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                   /*ob_size*/
    "{{ moduleName }}.{{ className }}",  /*tp_name*/
    sizeof({{ className }}),             /*tp_basicsize*/
    0,                                   /*tp_itemsize*/
    (destructor){{ className }}_dealloc, /*tp_dealloc*/
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
    "{{ className }} objects",           /* tp_doc */
    (traverseproc){{ className }}_traverse,   /* tp_traverse */
    (inquiry){{ className }}_clear,           /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    {{ className }}_methods,             /* tp_methods */
    {{ className }}_members,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc){{ className }}_init,      /* tp_init */
    0,                         /* tp_alloc */
    {{ className }}_new,                 /* tp_new */
};

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

    if (PyType_Ready(&{{ className }}Type) < 0)
        return;

    m = Py_InitModule3("{{ moduleName }}", module_methods,
                       "{{ moduleDescription }}");

    if (m == NULL)
      return;

    Py_INCREF(&{{ className }}Type);
    PyModule_AddObject(m, "{{ className }}", (PyObject *)&{{ className }}Type);
}