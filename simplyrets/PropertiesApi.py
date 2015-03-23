#!/usr/bin/env python

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

from models import *

class PropertiesApi(object):

    def __init__(self, apiClient):
      self.apiClient = apiClient


    def properties(self, **kwargs):
        """Retrieve property listings

        Args:
            brokers, list[str]: Listing brokerage or office. (optional)

            features, list[str]: Listing Features. (optional)

            amenities, list[str]: Listing Amentities. (optional)

            agent, list[str]: Listing (or Selling) Agent MLS Identifier. (optional)

            maxarea, long: Maximum property area. (optional)

            minarea, long: Minimum property area. (optional)

            minprice, long: Minimum Listing price to query (optional)

            minbaths, long: Minimum Number of baths (optional)

            maxbeds, long: Maximum Number of beds (optional)

            minbeds, long: Minimum Number of beds (optional)

            neighborhoods, byte: MLS Area or Location (Geomarket) (optional)

            points, list[float]: A list of latitude longitude
                coordinates which contain the property. Our documentation
                generator does not yet support using a list of
                parameters. Feel free to contact contact
                support@simplyrets.com for a query (optional)

            counties, list[str]: Filter properties by county. (optional)

            status, str: MLS Status (Data-Dictionary v1.3 compliant) (optional)

            type, str: The type of property listing. Default to Residential (optional)

            q, str: Query propertis with a fuzzy match.  Searches
                ListingId, PostalCode, Subdivision, City or Township and
                other fields depending on your MLS Standard Names
                support. (optional)

        Returns: list[Listing]
        """

        allParams = ['brokers', 'features', 'amenities', 'agent', 'maxarea',
                     'minarea', 'minprice', 'minbaths', 'maxbeds', 'minbeds',
                     'neighborhoods', 'points', 'counties', 'status', 'type', 'q']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method properties" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/properties'
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}
        formParams = {}
        files = {}
        bodyParam = None

        headerParams['Content-type'] = 'application/json'

        if ('brokers' in params):
            queryParams['brokers'] = self.apiClient.toPathValue(params['brokers'])
        if ('features' in params):
            queryParams['features'] = self.apiClient.toPathValue(params['features'])
        if ('amenities' in params):
            queryParams['amenities'] = self.apiClient.toPathValue(params['amenities'])
        if ('agent' in params):
            queryParams['agent'] = self.apiClient.toPathValue(params['agent'])
        if ('maxarea' in params):
            queryParams['maxarea'] = self.apiClient.toPathValue(params['maxarea'])
        if ('minarea' in params):
            queryParams['minarea'] = self.apiClient.toPathValue(params['minarea'])
        if ('minprice' in params):
            queryParams['minprice'] = self.apiClient.toPathValue(params['minprice'])
        if ('minbaths' in params):
            queryParams['minbaths'] = self.apiClient.toPathValue(params['minbaths'])
        if ('maxbeds' in params):
            queryParams['maxbeds'] = self.apiClient.toPathValue(params['maxbeds'])
        if ('minbeds' in params):
            queryParams['minbeds'] = self.apiClient.toPathValue(params['minbeds'])
        if ('neighborhoods' in params):
            queryParams['neighborhoods'] = self.apiClient.toPathValue(params['neighborhoods'])
        if ('points' in params):
            queryParams['points'] = self.apiClient.toPathValue(params['points'])
        if ('counties' in params):
            queryParams['counties'] = self.apiClient.toPathValue(params['counties'])
        if ('status' in params):
            queryParams['status'] = self.apiClient.toPathValue(params['status'])
        if ('type' in params):
            queryParams['type'] = self.apiClient.toPathValue(params['type'])
        if ('q' in params):
            queryParams['q'] = self.apiClient.toPathValue(params['q'])
        postData = (formParams if formParams else bodyParam)

        response = self.apiClient.callAPI(resourcePath, method, queryParams,
                                          postData, headerParams, files=files)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'list[Listing]')
        return responseObject


    def property(self, mlsId=None, **kwargs):
        """Retrieve a single listing

        Args:
            mlsId, int: Specify the mls number of the property. (required)

        Returns: Listing
        """

        allParams = ['mlsId']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method property" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/properties/{mlsId}'
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}
        formParams = {}
        files = {}
        bodyParam = None

        headerParams['Content-type'] = 'application/json'

        if ('mlsId' in params):
            replacement = str(self.apiClient.toPathValue(params['mlsId']))
            resourcePath = resourcePath.replace('{' + 'mlsId' + '}',
                                                replacement)
        postData = (formParams if formParams else bodyParam)

        response = self.apiClient.callAPI(resourcePath, method, queryParams,
                                          postData, headerParams, files=files)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'Listing')
        return responseObject
