// system
#include <math.h>
// python
#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif
// libeep
#include <v4/eep.h>
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_version(PyObject *self, PyObject *args)
{
  if (!PyArg_ParseTuple(args, ""))
  {
    return NULL;
  }

  return Py_BuildValue("s", libeep_get_version());
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_read(PyObject *self, PyObject *args)
{
  char *filename;

  if (!PyArg_ParseTuple(args, "s", &filename))
  {
    return NULL;
  }

  return Py_BuildValue("i", libeep_read_with_external_triggers(filename));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_write_cnt(PyObject *self, PyObject *args)
{
  char *filename;
  int rate;
  chaninfo_t channel_info_handle;
  int rf64;

  if (!PyArg_ParseTuple(args, "siii", &filename, &rate, &channel_info_handle, &rf64))
  {
    return NULL;
  }

  return Py_BuildValue("i", libeep_write_cnt(filename, rate, channel_info_handle, rf64));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_close(PyObject *self, PyObject *args)
{
  int handle;

  if (!PyArg_ParseTuple(args, "i", &handle))
  {
    return NULL;
  }

  libeep_close(handle);

  return Py_BuildValue("");
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_channel_count(PyObject *self, PyObject *args)
{
  int handle;

  if (!PyArg_ParseTuple(args, "i", &handle))
  {
    return NULL;
  }

  return Py_BuildValue("i", libeep_get_channel_count(handle));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_channel_label(PyObject *self, PyObject *args)
{
  int handle;
  int index;

  if (!PyArg_ParseTuple(args, "ii", &handle, &index))
  {
    return NULL;
  }

  return Py_BuildValue("s", libeep_get_channel_label(handle, index));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_channel_unit(PyObject *self, PyObject *args)
{
  int handle;
  int index;

  if (!PyArg_ParseTuple(args, "ii", &handle, &index))
  {
    return NULL;
  }

  return Py_BuildValue("s", libeep_get_channel_unit(handle, index));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_channel_reference(PyObject *self, PyObject *args)
{
  int handle;
  int index;

  if (!PyArg_ParseTuple(args, "ii", &handle, &index))
  {
    return NULL;
  }

  return Py_BuildValue("s", libeep_get_channel_reference(handle, index));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_sample_frequency(PyObject *self, PyObject *args)
{
  int handle;

  if (!PyArg_ParseTuple(args, "i", &handle))
  {
    return NULL;
  }

  return Py_BuildValue("i", libeep_get_sample_frequency(handle));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_sample_count(PyObject *self, PyObject *args)
{
  int handle;

  if (!PyArg_ParseTuple(args, "i", &handle))
  {
    return NULL;
  }

  return Py_BuildValue("i", libeep_get_sample_count(handle));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_samples(PyObject *self, PyObject *args)
{
  int handle;
  int fro;
  int to;

  Py_ssize_t i;

  if (!PyArg_ParseTuple(args, "iii", &handle, &fro, &to))
  {
    return NULL;
  }

  float *libeep_sample_data = libeep_get_samples(handle, fro, to);
  if (libeep_sample_data == NULL)
  {
    return NULL;
  }

  Py_ssize_t array_len = (to - fro) * libeep_get_channel_count(handle);
  PyObject *python_list = PyList_New(array_len);
  if (!python_list)
  {
    return NULL;
  }
  for (i = 0; i < array_len; i++)
  {
    PyObject *num = PyFloat_FromDouble(libeep_sample_data[i]);
    if (!num)
    {
      Py_DECREF(python_list);
      return NULL;
    }
    PyList_SET_ITEM(python_list, i, num); // reference to num stolen
  }
  libeep_free_samples(libeep_sample_data);
  return python_list;
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_add_samples(PyObject *self, PyObject *args)
{
  int handle;
  PyObject *obj;
  int channel_count;
  int i;
  int n;

  if (!PyArg_ParseTuple(args, "iOi", &handle, &obj, &channel_count))
  {
    return NULL;
  }

  n = PyList_Size(obj);
  float *local_data = (float *)malloc(sizeof(float) * n);
  for (i = 0; i < n; ++i)
  {
    local_data[i] = PyFloat_AsDouble(PyList_GetItem(obj, i));
  }
  libeep_add_samples(handle, local_data, n / channel_count);
  free(local_data);

  return Py_BuildValue("");
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_trigger_count(PyObject *self, PyObject *args)
{
  int handle;

  if (!PyArg_ParseTuple(args, "i", &handle))
  {
    return NULL;
  }

  return Py_BuildValue("i", libeep_get_trigger_count(handle));
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_get_trigger(PyObject *self, PyObject *args)
{
  int handle;
  int index;

  if (!PyArg_ParseTuple(args, "ii", &handle, &index))
  {
    return NULL;
  }

  uint64_t sample;
  const char *trigger;
  struct libeep_trigger_extension te;
  trigger = libeep_get_trigger_with_extensions(handle, index, &sample, &te);

  return Py_BuildValue("siisss", trigger, sample, te.duration_in_samples, te.condition, te.description, te.impedances);
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_create_channel_info(PyObject *self, PyObject *args)
{
  if (!PyArg_ParseTuple(args, ""))
  {
    return NULL;
  }

  return Py_BuildValue("i", libeep_create_channel_info());
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_close_channel_info(PyObject *self, PyObject *args)
{
  int handle;

  if (!PyArg_ParseTuple(args, "i", &handle))
  {
    return NULL;
  }

  libeep_close_channel_info(handle);

  return Py_BuildValue("");
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_add_channel(PyObject *self, PyObject *args)
{
  int handle;
  char *label;
  char *ref_label;
  char *unit;

  if (!PyArg_ParseTuple(args, "isss", &handle, &label, &ref_label, &unit))
  {
    return NULL;
  }

  libeep_add_channel(handle, label, ref_label, unit);

  return Py_BuildValue("");
}
///////////////////////////////////////////////////////////////////////////////
static PyObject *
pyeep_add_trigger(PyObject *self, PyObject *args)
{
  int handle;
  unsigned int sample;
  char *code;
  int ret;

  if (!PyArg_ParseTuple(args, "iIs", &handle, &sample, &code))
  {
    return NULL;
  }

  ret = libeep_add_trigger(handle, sample, code);

  return Py_BuildValue("i", ret);
}
///////////////////////////////////////////////////////////////////////////////
static PyMethodDef methods[] = {
    {"get_version", pyeep_get_version, METH_VARARGS, "get libeep version"},
    {"read", pyeep_read, METH_VARARGS, "open libeep file for reading"},
    {"write_cnt", pyeep_write_cnt, METH_VARARGS, "open libeep cnt file for writing"},
    {"close", pyeep_close, METH_VARARGS, "close handle"},
    {"get_channel_count", pyeep_get_channel_count, METH_VARARGS, "get channel count"},
    {"get_channel_label", pyeep_get_channel_label, METH_VARARGS, "get channel label"},
    {"get_channel_unit", pyeep_get_channel_unit, METH_VARARGS, "get channel unit"},
    {"get_channel_reference", pyeep_get_channel_reference, METH_VARARGS, "get channel reference"},
    // float libeep_get_channel_scale(cntfile_t handle, int index);
    // int libeep_get_channel_index(cntfile_t handle, const char *label);
    {"get_sample_frequency", pyeep_get_sample_frequency, METH_VARARGS, "get sample frequency"},
    {"get_sample_count", pyeep_get_sample_count, METH_VARARGS, "get sample count"},
    {"get_samples", pyeep_get_samples, METH_VARARGS, "get samples"},
    {"add_samples", pyeep_add_samples, METH_VARARGS, "add samples"},
    // void libeep_add_raw_samples(cntfile_t handle, const int32_t *data, int n);
    // int32_t * libeep_get_raw_samples(cntfile_t handle, long from, long to);
    // void libeep_free_raw_samples(int32_t *data);
    // recinfo_t libeep_create_recinfo();
    // void libeep_add_recording_info(cntfile_t cnt_handle, recinfo_t recinfo_handle);
    // time_t libeep_get_start_time(cntfile_t handle);
    // void libeep_get_start_date_and_fraction(recinfo_t handle, double* start_date, double* start_fraction);
    // void libeep_set_start_time(recinfo_t handle, time_t start_time);
    // void libeep_set_start_date_and_fraction(recinfo_t handle, double start_date, double start_fraction);
    // const char *libeep_get_hospital(cntfile_t handle);
    // void libeep_set_hospital(recinfo_t handle, const char *value);
    // const char *libeep_get_test_name(cntfile_t handle);
    // void libeep_set_test_name(recinfo_t handle, const char *value);
    // const char *libeep_get_test_serial(cntfile_t handle);
    // void libeep_set_test_serial(recinfo_t handle, const char *value);
    // const char *libeep_get_physician(cntfile_t handle);
    // void libeep_set_physician(recinfo_t handle, const char *value);
    // const char *libeep_get_technician(cntfile_t handle);
    // void libeep_set_technician(recinfo_t handle, const char *value);
    // const char *libeep_get_machine_make(cntfile_t handle);
    // void libeep_set_machine_make(recinfo_t handle, const char *value);
    // const char *libeep_get_machine_model(cntfile_t handle);
    // void libeep_set_machine_model(recinfo_t handle, const char *value);
    // const char *libeep_get_machine_serial_number(cntfile_t handle);
    // void libeep_set_machine_serial_number(recinfo_t handle, const char *value);
    // const char *libeep_get_patient_name(cntfile_t handle);
    // void libeep_set_patient_name(recinfo_t handle, const char *value);
    // const char *libeep_get_patient_id(cntfile_t handle);
    // void libeep_set_patient_id(recinfo_t handle, const char *value);
    // const char *libeep_get_patient_address(cntfile_t handle);
    // void libeep_set_patient_address(recinfo_t handle, const char *value);
    // const char *libeep_get_patient_phone(cntfile_t handle);
    // void libeep_set_patient_phone(recinfo_t handle, const char *value);
    // const char *libeep_get_comment(cntfile_t handle);
    // void libeep_set_comment(recinfo_t handle, const char *value);
    // char libeep_get_patient_sex(cntfile_t handle);
    // void libeep_set_patient_sex(recinfo_t handle, char value);
    // char libeep_get_patient_handedness(cntfile_t handle);
    // void libeep_set_patient_handedness(recinfo_t handle, char value);
    // void libeep_get_date_of_birth(cntfile_t handle, int * year, int * month, int *day);
    // void libeep_set_date_of_birth(recinfo_t handle, int year, int month, int day);
    // int libeep_add_trigger(cntfile_t handle, uint64_t sample, const char *code);
    {"add_trigger", pyeep_add_trigger, METH_VARARGS, "add trigger"},
    {"get_trigger_count", pyeep_get_trigger_count, METH_VARARGS, "get trigger count"},
    {"get_trigger", pyeep_get_trigger, METH_VARARGS, "get samples"},
    // long libeep_get_zero_offset(cntfile_t handle);
    // const char * libeep_get_condition_label(cntfile_t handle);
    // const char * libeep_get_condition_color(cntfile_t handle);
    // long libeep_get_trials_total(cntfile_t handle);
    // long libeep_get_trials_averaged(cntfile_t handle);
    {"create_channel_info", pyeep_create_channel_info, METH_VARARGS, "create channel info handle"},
    {"close_channel_info", pyeep_close_channel_info, METH_VARARGS, "close channel info handle"},
    {"add_channel", pyeep_add_channel, METH_VARARGS, "add channel to channel info handle"},
    {NULL, NULL, 0, NULL}};
///////////////////////////////////////////////////////////////////////////////
// module initialization
#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "pyeep",
    NULL,
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL};
#define INITERROR return NULL
PyMODINIT_FUNC PyInit_pyeep(void)
{
#else
#define INITERROR return
PyMODINIT_FUNC initpyeep(void)
{
#endif
  // init libeep
  libeep_init();

  // register methods
#if PY_MAJOR_VERSION >= 3
  PyObject *module = PyModule_Create(&moduledef);
#else
  PyObject *module = Py_InitModule("pyeep", methods);
#endif

  if (module == NULL)
  {
    INITERROR;
  }

#if PY_MAJOR_VERSION >= 3
  return module;
#endif
}
