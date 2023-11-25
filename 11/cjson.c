#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>


PyObject* cjson_loads(PyObject* self, PyObject* args)
{
    char* str_p;

    if (!PyArg_ParseTuple(args, "s", &str_p)){
        PyErr_Format(PyExc_TypeError, "Expected JSON object");
        return NULL;
    }

    if (*str_p != '{') {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON object: no opening parenthesis");
        return NULL;
    }

    PyObject *dict = NULL;

    if (!(dict = PyDict_New())) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create Dict object");
        return NULL;
    }

    str_p++;

    PyObject* value = NULL;
    PyObject* key = NULL;

    while (*str_p != '\0' && *str_p != '}') {

         // find key
        if (*str_p == ' '){
            str_p++;
            continue;
        }

        if (*str_p != '"'){
            PyErr_SetString(PyExc_ValueError, "Failed to build string for key");
            Py_DECREF(dict);
            return NULL;
        }

        str_p++;

        char* start_key = str_p;
        long size_key = 0;

        while (*str_p != '\0' && *str_p != '"'){
            str_p++;
            size_key++;
        }

        if (*str_p == '\0' || *str_p != '"') {
            PyErr_SetString(PyExc_ValueError, "Failed to build string for key");
            Py_DECREF(dict);
            return NULL;
        }

        if (!(key = Py_BuildValue("s#", start_key, size_key))) {
            PyErr_SetString(PyExc_ValueError, "Failed to build string for key");
            Py_DECREF(dict);
            return NULL;
        }

        // find value
        str_p++;

        while (*str_p != '\0' && *str_p == ' '){
            str_p++;
        }

        if (*str_p != ':'){
            PyErr_SetString(PyExc_ValueError, "Invalid JSON object: semicolon not found");
            Py_DECREF(dict);
            return NULL;
        }
        str_p++;

        while (*str_p != '\0' && *str_p == ' '){
            str_p++;
        }

        if (*str_p == '"'){
            str_p++;

            char* start_value = str_p;
            long size_value = 0;

            while (*str_p != '\0' && *str_p != '"'){
                str_p++;
                size_value++;
            }

            if (*str_p == '\0' || *str_p != '"') {
                PyErr_SetString(PyExc_ValueError, "Failed to build string for value");
                Py_DECREF(dict);
                return NULL;
            }

            if (!(value = Py_BuildValue("s#", start_value, size_value))) {
                PyErr_SetString(PyExc_ValueError, "Failed to build string for value");
                Py_DECREF(dict);
                return NULL;
            }

            str_p++;

        }
        else if ((*str_p >= '0' && *str_p <= '9') || (*str_p == '-')){
            long l_value = 0;
            bool flag = false;

            if (*str_p == '-'){
                flag = true;
                str_p++;
            }

            while (*str_p != '\0' && *str_p >= '0' && *str_p <= '9'){
                l_value = l_value * 10 + ((int)*str_p - (int)'0');
                str_p++;
            }

            if (*str_p == '\0') {
                PyErr_SetString(PyExc_ValueError, "Failed to build integer for value");
                Py_DECREF(dict);
                return NULL;
            }

            if (flag == true){
                l_value *= -1;
            }

            if (!(value = Py_BuildValue("l", l_value))) {
                PyErr_SetString(PyExc_ValueError, "Failed to build integer for value");
                Py_DECREF(dict);
                return NULL;
            }

        }
        else{
            PyErr_SetString(PyExc_ValueError, "Failed to build value");
            Py_DECREF(dict);
            return NULL;
        }

        if (PyDict_SetItem(dict, key, value) < 0) {
            PyErr_Format(PyExc_TypeError, "Failed to set item");
            Py_DECREF(dict);
            return NULL;
        }

       Py_DECREF(key);
       Py_DECREF(value);

       while (*str_p != '\0' && *str_p == ' '){
            str_p++;
            }

       if (*str_p == '}'){
           continue;
       }

       if (*str_p == '\0' || *str_p != ',') {
           PyErr_SetString(PyExc_ValueError, "Invalid JSON object: comma not found");
           Py_DECREF(dict);
           return NULL;
       }
       str_p++;
    }

    if (*str_p == '\0' || *str_p != '}') {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON object: no closing parenthesis");
        Py_DECREF(dict);
        return NULL;

    }

    return dict;
};

static PyObject* cjson_dumps(PyObject* self, PyObject* args)
 {
    PyObject* obj;

    if (!PyArg_ParseTuple(args, "O", &obj) || !PyDict_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument");
        return NULL;
    }

    PyObject* items = PyDict_Items(obj);

    if (items == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to get dictionary items");
        return NULL;
    }

    long num_items = PyList_Size(items);
    size_t size = 4;

    // find size of json-str
    for (long i = 0; i < num_items; i++) {

        PyObject* item = PyList_GetItem(items, i);

        if (item == NULL) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to get item from list");
            Py_DECREF(items);
            return NULL;
        }

        PyObject* key = PyTuple_GetItem(item, 0);
        PyObject* value = PyTuple_GetItem(item, 1);

        if (!PyUnicode_Check(key)) {
            PyErr_SetString(PyExc_TypeError, "Key must be a string");
            Py_DECREF(items);
            return NULL;
        }

        char* key_str = PyUnicode_AsUTF8(key);
        size += strlen(key_str) + 4;

        if (PyLong_Check(value)) {
            size += 25;
        }
        else if (PyUnicode_Check(value)){
            const char* value_str = PyUnicode_AsUTF8(value);
            size += strlen(value_str) + 2;
        }
        else{
            PyErr_SetString(PyExc_TypeError, "Value must be a number or a string");
            Py_DECREF(items);
            return NULL;
        }
    }
    // writing json-str
    char* json = malloc(size);
    json[0] = '\0';

    size_t json_len = 0;
    memcpy(json + json_len, "{", 1);
    json_len += 1;

    for (long i = 0; i < num_items; i++) {

        PyObject* item = PyList_GetItem(items, i);
        PyObject* key = PyTuple_GetItem(item, 0);
        PyObject* value = PyTuple_GetItem(item, 1);

        char* key_str = PyUnicode_AsUTF8(key);
        size_t key_len = strlen(key_str);

        memcpy(json + json_len, "\"", 1);
        memcpy(json + json_len + 1, key_str, key_len);
        memcpy(json + json_len + 1 + key_len, "\":", 2);

        json_len += key_len + 3;

        if (PyLong_Check(value)) {
            long value_long = PyLong_AsLong(value);
            char value_str[25];
            int value_len = snprintf(value_str, sizeof(value_str), "%ld", value_long);

            memcpy(json + json_len, value_str, value_len);

            json_len += value_len;

        }
        else {
            char* value_str = PyUnicode_AsUTF8(value);
            size_t value_len = strlen(value_str);

            memcpy(json + json_len, "\"", 1);
            memcpy(json + json_len + 1, value_str, value_len);
            memcpy(json + json_len + 1 + value_len, "\"", 1);

            json_len += value_len + 2;
        }

        if (i < num_items - 1) {
            memcpy(json + json_len, ",", 1);
            json_len += 1;
        }
    }

    memcpy(json + json_len, "}", 1);

    json_len += 1;
    json[json_len] = '\0';

    Py_DECREF(items);
    return Py_BuildValue("s", json);
};

//final stage
static PyMethodDef cjson_methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Deserialize JSON string to dictionary"},
    {"dumps", cjson_dumps, METH_VARARGS, "Serialize dictionary to JSON string"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cjson_module = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    NULL,
    -1,
    cjson_methods

};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson_module);
};