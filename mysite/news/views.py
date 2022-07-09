from django.shortcuts import render
from django.http import HttpResponse
import requests
import hashlib
import re
from django.template import context
from elasticsearch import Elasticsearch
from datetime import datetime
from collections import Counter
import time
import pprint
import json
import numpy as np


# Create your views here.
def index(request):
    print(request)
    return HttpResponse('<h3>LOLOLOLO<br>asdfghjkl</h3>')


def test(request):
    print(request)
    client = Elasticsearch("http://192.168.56.101:9200")

    query_body = {
        "_source": {
            "excludes": ["who.spt", "who.dpt"]},
        "query": {
            "range": {
                "timestamp": {
                    "gte": 1652625057050,
                    "lte": 1652625057650
                }
            }
        }
    }

    result = client.search(index="security_events_1_19127", body=query_body, size=1000)
    arr = []

    for hit in result['hits']['hits']:
        str0 = '\n '.join(
            ' = '.join((key, val)) for (key, val) in hit["_source"]["what"].items()) + ' +++ ' + '\n '.join(
            ' = '.join((key, val)) for (key, val) in hit["_source"]["who"].items()) + ' +++ ' + '\n '.join(
            ' = '.join((key, val)) for (key, val) in hit["_source"]["where"].items())
        arr.append(str0)

    b = set(arr)
    values, counts = np.unique(arr, return_counts=True)

    separator = ' +++ '
    arr1 = []

    for i in range(len(values)):
        strstr = values[i].split(separator)
        arr1.append(strstr)

    what = []
    where = []
    who = []

    for i in range(len(arr1)):
        s = arr1[i][0]
        what.append(s)
        d = arr1[i][1]
        where.append(d)
        f = arr1[i][2]
        who.append(f)

    new_separator = '\n '
    new_what = []
    for i in range(len(what)):
        new_newstring = what[i].split(new_separator)
        new_what.append(new_newstring)

    for i in range(len(new_what)):
        for j in range(len(new_what[i])):
            if "text" in new_what[i][j]:
                new_what[i][0], new_what[i][j] = new_what[i][j], new_what[i][0]

    string123 = ""
    duken = []
    for i in range(len(new_what)):
        for j in range(len(new_what[i])):
            string123 = string123 + new_what[i][j] + "\n"
        duken.append(string123)
        string123 = ""

    for i in range(len(duken)):
        if "text" in duken[i]:
            duken[i] = re.sub('text', '<mark><font size="3"><b> text </b></font></mark>', duken[i])

    mylist = zip(duken, who, where, counts)
    return render(request, 'news/shablon.html', {'mylist': mylist})


def qw(request):
    print(request)
    return render(request, 'news/jai.html')
