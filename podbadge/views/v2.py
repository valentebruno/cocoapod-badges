__author__ = 'flaviocaetano'

from django.shortcuts import render_to_response, redirect
from django.utils import simplejson

import os, urllib2, StringIO

def version(request, podname):
    try:
        pod_info = get_pod_info(podname)

        version = pod_info['version']
    except urllib2.HTTPError, e:
        if e.code == 404:
            return redirect('/v1/%s/badge.png' % podname)

        version = 'error'
            
    except Exception, e:
        version = 'error'

    width = 63+5*len(version)
    total_width = 73 + width

    return render_to_response('badge_version.html', {
        'VERSION':version,
        'WIDTH': 63+5*len(version),
        'TOTAL_WIDTH': total_width,
    }, mimetype="image/svg+xml")

def platform(request, podname):
    try:
        pod_info = get_pod_info(podname)

        platforms = pod_info['platforms'].keys()
        width = 80 if len(platforms) == 1 else 104

        platforms = '/'.join(platforms)
    except Exception, e:
        platforms = 'error'
        width = 90

    total_width = 73 + width

    return render_to_response('badge_platform.html', {
        'PLATFORM':platforms,
        'WIDTH': width,
        'TOTAL_WIDTH': total_width,
    }, mimetype="image/svg+xml")

def badge(request, info, podname):
    if info == 'p':
        return platform(request, podname)

    return version(request, podname)

def get_pod_info(podname):
    url = 'http://cocoapods.org/api/v1/pod/%s.json' % (podname, )

    response = urllib2.urlopen(url)
    return simplejson.loads(response.read())