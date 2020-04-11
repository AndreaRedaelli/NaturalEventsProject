import requests
import json
import pandas as pd
import datetime
import xml.etree.ElementTree as ElementTree

#EONET is a repository of metadata about natural events. 
endpoint = 'https://eonet.sci.gsfc.nasa.gov/api/v2.1/events'

def callWS(limit,days,source,status):
    try:
        session = requests.Session()
        response = session.get(endpoint,params={'limit': limit,'days': days,'source': source,'status':status})  
        #if you want more information you can print status code
        #print(req.status_code)
        data = json.loads(response.text)
        print(len(data['events']))
        listaCategories = []
        listaFirstEventInsert = []
        listaLastEventInsert = []
        listaGeoJsonFirst = []
        listaGeoJsonLast = []
        listaTypeGeoFirst = []
        listaTypeGeoLast = []
        listaTitoli = []
        matrice = None
        for d in data['events']:
            listaCategories.append(dict(d['categories'][0])['title'])
            #use a lambda function to order the geometries
            ListOrderedGeom = sorted(d['geometries'], key = lambda i: datetime.datetime.strptime(i['date'], '%Y-%m-%dT%H:%M:%SZ'))  
            if(len(ListOrderedGeom) >=2):
                listaFirstEventInsert.append(ListOrderedGeom[0]['date'])
                listaLastEventInsert.append(ListOrderedGeom[len(ListOrderedGeom)-1]['date'])
                listaGeoJsonFirst.append(ListOrderedGeom[0]['coordinates'])
                listaTypeGeoFirst.append(ListOrderedGeom[0]['type'])
                listaGeoJsonLast.append(ListOrderedGeom[len(ListOrderedGeom)-1]['coordinates'])
                listaTypeGeoLast.append(ListOrderedGeom[len(ListOrderedGeom)-1]['type'])
            else:
                listaFirstEventInsert.append(ListOrderedGeom[0]['date'])
                listaLastEventInsert.append(ListOrderedGeom[0]['date'])
                listaGeoJsonFirst.append(ListOrderedGeom[0]['coordinates'])
                listaTypeGeoFirst.append(ListOrderedGeom[0]['type'])
                listaGeoJsonLast.append(ListOrderedGeom[0]['coordinates'])
                listaTypeGeoLast.append(ListOrderedGeom[0]['type'])

            listaTitoli.append(d['title'])
            #print(listaTitoli)
        matrice = {'Title' : listaTitoli, 'Category' : listaCategories,
         'FirstTimeEventOccour':listaFirstEventInsert, 'FirstEventGeoJson':listaGeoJsonFirst, 'GeoJsonType':listaTypeGeoFirst,
         'LastTimeEventOccour': listaLastEventInsert,'LastEventGeoJson': listaGeoJsonLast, 'GeoJsonType':listaTypeGeoLast}
        # Set it None to pd.set_option('display.max_rows', None)
        pd.set_option('display.max_rows', None)
        dataframe = pd.DataFrame(data=matrice)
        return dataframe

    except:
        
        raise

#GIBS is Global Imagery Browse Services see https://wiki.earthdata.nasa.gov/display/GIBS/GIBS+API+for+Developers
# I choose to use : 
# best -> The "Best Available" imagery products.
# wms -> Open Geospatial Consortium (OGC) Web Map Service (WMS) which supports a key-value-pair non-tiled requests
# epsg -> 3857 EPSG:3857 - Web Mercator / Spherical Mercator / "Google Projection"
endpointGetCapabilities = 'https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0'

def callWSGetCapabilities():
    try:
        listaNames = []
        session = requests.Session()
        response = session.get(endpointGetCapabilities)  
        root = ElementTree.fromstring(response.content)
        for child in root.iter('{http://www.opengis.net/wms}Layer'):
            nestedRoot = child
            for childNested in nestedRoot:
                if (childNested.tag == '{http://www.opengis.net/wms}Name' and childNested.text != "default"):
                    listaNames.append(childNested.text)  
        print(len(listaNames))
        return listaNames
    except:
        
        raise
def GetImage(layers,format,styles,bbox,crs,width,height,transparent,time):
    try:
        endpoint ="https://gibs.earthdata.nasa.gov/wms/epsg4326/all/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&" + "LAYERS=" + layers + "&STYLES=&FORMAT=" + format + "&TRANSPARENT=true&HEIGHT="+height+"&WIDTH=256&TIME=" + time + "&CRS=EPSG:4326&BBOX=" + bbox
        #print(endpoint)
        session = requests.Session()
        response = session.get(endpoint)
        #response = session.get("https://gibs.earthdata.nasa.gov/wms/epsg4326/all/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS=VIIRS_SNPP_CorrectedReflectance_TrueColor&STYLES=&FORMAT=image%2Fpng&TRANSPARENT=true&HEIGHT=256&WIDTH=256&TIME=2020-03-01&CRS=EPSG:4326&BBOX=-61,-81,-28,-48")  
        return response
    except:
        
        raise