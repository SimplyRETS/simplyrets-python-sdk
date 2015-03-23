#!/usr/bin/env python

__author__ = "Christopher and Cody Reichert"
__copyright__ = "Copyright 2015, SimplyRETS Inc. <support@simplyrets.com>"
__credits__ = ["Christopher Reichert", "Cody Reichert"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Christopher Reichert"
__email__ = "christopher@simplyrets.com"
__status__ = "Production"

class Property:
    """ NOTE: This class is auto generated by the SimplyRets code
              generator program.  Do not edit the class manually.
    """

    def __init__(self):
        self.simplyRetsTypes = {
            'roof': 'str',
            'style': 'str',
            'area': 'long',
            'bathsFull': 'long',
            'bathsHalf': 'long',
            'stories': 'float',
            'fireplaces': 'long',
            'heating': 'str',
            'bedrooms': 'long',
            'interiorFeatures': 'str',
            'lotSize': 'str',
            'exteriorFeatures': 'str',
            'subdivision': 'str',
            'type': 'str',
            'yearBuilt': 'long'

        }

        # Property roof description
        self.roof = None # str
        # Property style description or short string
        self.style = None # str
        # Square footage of the building associated with a listing
        self.area = None # long
        # Number of full bathrooms
        self.bathsFull = None # long
        # Number of half bathrooms
        self.bathsHalf = None # long
        # Number of stories or levels. Represented as a `double' to account for half stories.
        self.stories = None # float
        # Number of fireplaces
        self.fireplaces = None # long
        # Heating description or short string
        self.heating = None # str
        # Number of bedrooms
        self.bedrooms = None # long
        # The properties interior features
        self.interiorFeatures = None # str
        # Square footage of the entire property lot
        self.lotSize = None # str
        self.exteriorFeatures = None # str
        # The subdivision or community name
        self.subdivision = None # str
        # Property type (Residential, Multi-Family, Rental)
        self.type = None # str
        # Year the property was built
        self.yearBuilt = None # long