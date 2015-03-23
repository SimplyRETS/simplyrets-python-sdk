#!/usr/bin/env python

"""SimplyRETS SDK API client."""

__author__ = "Christopher and Cody Reichert"
__copyright__ = "Copyright 2015, SimplyRETS Inc. <support@simplyrets.com>"
__credits__ = ["Christopher Reichert", "Cody Reichert"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Christopher Reichert"
__email__ = "christopher@simplyrets.com"
__status__ = "Production"

import sys
import os
import re
import urllib
import urllib2
import httplib
import json
import datetime
import mimetypes
import random
import string
import base64

from models import *


class Connection:
    """SimplRETS API Client Connection"""

    def __init__(self, apiKey=None, apiSecret=None):
        if apiKey == None:
            raise Exception('You must pass an apiKey when instantiating the API Connection')
        if apiSecret == None:
            raise Exception('You must pass an apiSecret when instantiating the API Connection')
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.apiServer = 'https://api.simplyrets.com'
        self.cookie = None
        self.boundary = ''.join(random.choice(string.ascii_letters + string.digits)
                                    for _ in range(30))

    def callAPI(self, resourcePath, method, queryParams, postData,
                headerParams=None, files=None):

        url = self.apiServer + resourcePath
        headers = {}
        if headerParams:
            for param, value in headerParams.iteritems():
                headers[param] = value

        # Specify API Version
        #headers['Content-type'] = 'application/vnd.simplyrets-v0.1+json'

        # Encode HTTP Basic Authentication Header
        encodedAuth = base64.b64encode(self.apiKey + ':' + self.apiSecret)
        headers['Authorization'] = 'Basic ' + encodedAuth

        if self.cookie:
            headers['Cookie'] = self.cookie

        data = None

        if queryParams:
            # Need to remove None values, these should not be sent
            sentQueryParams = {}
            for param, value in queryParams.items():
                if value != None:
                    sentQueryParams[param] = value
            url = url + '?' + urllib.urlencode(sentQueryParams, True)

        if method in ['GET']:

            #Options to add statements later on and for compatibility
            pass

        elif method in ['POST', 'PUT', 'DELETE']:

            if postData:
                postData = self.sanitizeForSerialization(postData)
                if 'Content-type' not in headers:
                    headers['Content-type'] = 'application/json'
                    data = json.dumps(postData)
                elif headers['Content-type'] == 'multipart/form-data':
                    data = self.buildMultipartFormData(postData, files)
                    headers['Content-type'] = 'multipart/form-data; boundary={0}'.format(self.boundary)
                    headers['Content-length'] = str(len(data))
                else:
                    data = urllib.urlencode(postData)
        else:
            raise Exception('Method ' + method + ' is not recognized.')

        request = MethodRequest(method=method, url=url, headers=headers, data=data)

        # Make the request
        response = urllib2.urlopen(request)
        if 'Set-Cookie' in response.headers:
            self.cookie = response.headers['Set-Cookie']
        string = response.read()

        try:
            data = json.loads(string)
        except ValueError:  # PUT requests don't return anything
            data = None

        return data

    def toPathValue(self, obj):
        """Convert a string or object to a path-friendly value
        Args:
            obj -- object or string value
        Returns:
            string -- quoted value

        NOTE: urllib.quote mixed with urllib.urlencode has
              strange behavior https://bugs.python.org/issue13866
        """
        if type(obj) == list:
            # return [ urllib.quote(x) for x in obj]
            return [ str(x) for x in obj]
        else:
            # return urllib.quote(str(obj))
            return str(obj)

    def sanitizeForSerialization(self, obj):
        """Dump an object into JSON for POSTing."""

        if type(obj) == type(None):
            return None
        elif type(obj) in [str, int, long, float, bool]:
            return obj
        elif type(obj) == list:
            return [self.sanitizeForSerialization(subObj) for subObj in obj]
        elif type(obj) == datetime.datetime:
            return obj.isoformat()
        else:
            if type(obj) == dict:
                objDict = obj
            else:
                objDict = obj.__dict__
            return {key: self.sanitizeForSerialization(val)
                    for (key, val) in objDict.iteritems()
                    if key != 'simplyRetsTypes'}

        if type(postData) == list:
            # Could be a list of objects
            if type(postData[0]) in safeToDump:
                data = json.dumps(postData)
            else:
                data = json.dumps([datum.__dict__ for datum in postData])
        elif type(postData) not in safeToDump:
            data = json.dumps(postData.__dict__)

    def buildMultipartFormData(self, postData, files):
        def escape_quotes(s):
            return s.replace('"', '\\"')

        lines = []

        for name, value in postData.items():
            lines.extend((
                '--{0}'.format(self.boundary),
                'Content-Disposition: form-data; name="{0}"'.format(escape_quotes(name)),
                '',
                str(value),
            ))

        for name, filepath in files.items():
            f = open(filepath, 'r')
            filename = filepath.split('/')[-1]
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            lines.extend((
                '--{0}'.format(self.boundary),
                'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(escape_quotes(name), escape_quotes(filename)),
                'Content-Type: {0}'.format(mimetype),
                '',
                f.read()
            ))

        lines.extend((
            '--{0}--'.format(self.boundary),
            ''
        ))
        return '\r\n'.join(lines)


    def deserialize(self, obj, objClass):
      """Derialize a JSON string into an object.

      Args:
          obj -- string or object to be deserialized
          objClass -- class literal for deserialzied object, or string
              of class name
      Returns:
          object -- deserialized object"""

      # Have to accept objClass as string or actual type. Type could be a
      # native Python type, or one of the model classes.
      if type(objClass) == str:
        if 'list[' in objClass:
          match = re.match('list\[(.*)\]', objClass)
          subClass = match.group(1)
          return [self.deserialize(subObj, subClass) for subObj in obj]

        if (objClass in ['int', 'float', 'long', 'dict', 'list', 'str', 'bool', 'datetime']):
          objClass = eval(objClass)
        else:  # not a native type, must be model class
          objClass = eval(objClass + '.' + objClass)

      if objClass in [int, long, float, dict, list, str, bool]:
        return objClass(obj)
      elif objClass == datetime:
        # Server will always return a time stamp in UTC, but with
        # trailing +0000 indicating no offset from UTC. So don't process
        # last 5 characters.
        return datetime.datetime.strptime(obj[:-5], "%Y-%m-%dT%H:%M:%S")

      instance = objClass()

      for attr, attrType in instance.simplyRetsTypes.iteritems():
          if obj is not None and attr in obj and type(obj) in [list, dict]:
            value = obj[attr]
            if attrType in ['str', 'int', 'long', 'float', 'bool']:
              attrType = eval(attrType)
              try:
                value = attrType(value)
              except UnicodeEncodeError:
                value = unicode(value)
              except TypeError:
                value = value
              setattr(instance, attr, value)
            elif (attrType == 'datetime'):
              setattr(instance, attr,
                      datetime.datetime.strptime(value[:-5],
                                                 "%Y-%m-%dT%H:%M:%S"))
            elif 'list[' in attrType:
              match = re.match('list\[(.*)\]', attrType)
              subClass = match.group(1)
              subValues = []
              if not value:
                setattr(instance, attr, None)
              else:
                for subValue in value:
                  subValues.append(self.deserialize(subValue, subClass))
              setattr(instance, attr, subValues)
            else:
              setattr(instance, attr, self.deserialize(value, attrType))

      return instance



class MethodRequest(urllib2.Request):

    def __init__(self, *args, **kwargs):
        """Construct a MethodRequest. Usage is the same as for
        `urllib2.Request` except it also takes an optional `method`
        keyword argument. If supplied, `method` will be used instead of
        the default."""

        if 'method' in kwargs:
            self.method = kwargs.pop('method')
        return urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return getattr(self, 'method', urllib2.Request.get_method(self))
