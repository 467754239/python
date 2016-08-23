# -*- coding: utf-8 -*-
from __future__ import unicode_literals


"""
Utility programmes to,
      1. Convert any json data file to Elasticsearch bulk upload json format.
      1. Bulk upload to Elasticsearch using elasticsearch.helpers.bulk API.
"""

import json
from elasticsearch import Elasticsearch 
from elasticsearch.helpers import bulk


"""
Used for converting json data file to ES bulk upload json format.
Parameters:
1. Elasticsearch Index Name
2. Elasticsearch Type Name
3. JSON data file (input)
4. Elasticsearch format JSON file (output)
"""
def convert_to_es_json(es_index, es_type, in_file, out_file):
      with open(in_file, 'r') as i_fp:
            data = json.load(i_fp)

      index_id = 0
      with open(out_file, 'w') as o_fp:
            for record in data:
                  index_id += 1
                  o_fp.write('{ "index":' + ' { "_index" : "'+  es_index + '", "_type" : "' +  es_type + '", "_id" : '\
                             + '%d' % index_id + '} }\n')
                  json.dump(record, o_fp)
                  o_fp.write('\n')

      return index_id

"""
Used for bulk upload of json data to Elasticsearch.
Parameters:
1. Elasticsearch Index Name
2. Elasticsearch Type Name
3. JSON data file (input)
"""
def bulk_post_to_es(es_index, es_type, in_file):
      with open(in_file, 'r') as i_fp:          
            es = Elasticsearch([{'host' : 'localhost'}, {'port' : 9200}])
            bulk_data = []
            index_id = 0

            json_data = json.load(i_fp)

            for item in json_data:
                  bulk_data.append({"_op_type": "index", \
                                    "_index" : es_index, \
                                    "_type" : es_type, \
                                    "_id" : index_id+1, \
                                    "doc" : json_data[index_id]})
                                    
                  index_id += 1

            bulk(es, bulk_data)
            return index_id

if __name__ == '__main__':
      print '*** Converting json data to Elasticsearch \'bulk\' json format. ***'

      retVal = convert_to_es_json('streamflix_movies', 'title', 'c:\es_code\data\streamflix_movies.json', 'c:\es_code\data\streamflix_movies_es.json')
      print retVal, ' items converted...'
      
      retVal = convert_to_es_json('profs', 'name', 'c:\es_code\data\profs.json', 'c:\es_code\data\profs_es.json')
      print retVal, ' items converted...'

      print '*** Bulk posting the data to Elasticsearch. ***'

      retVal = bulk_post_to_es('streamflix_movies', 'title', 'c:\es_code\data\streamflix_movies.json')
      print retVal, ' items posted in bulk...'

      retVal = bulk_post_to_es('profs', 'name', 'c:\es_code\data\profs.json')
      print retVal, ' items posted in bulk...'