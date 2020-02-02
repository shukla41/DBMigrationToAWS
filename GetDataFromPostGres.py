import psycopg2
import collections
from flask import Flask, request, make_response
from flask_restful import Resource, Api
import sys
import json
from json import dumps
from flask.json import jsonify

app = Flask(__name__)
api = Api(app)

class srcMetaDataInfo(Resource):

    def get(self,*argv):
        names_as_dict = []
        arg=argv
        try:
            connection = psycopg2.connect(user = "shuva",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "guru99")
            cursor = connection.cursor()
            create_table_query = ""'''SELECT ordinal_position, tab_columns.column_name, data_type, character_maximum_length,
                                                        numeric_precision, is_nullable, tab_constraints.constraint_type
                                                        FROM information_schema.columns AS tab_columns
                                                        LEFT OUTER JOIN
                                                        information_schema.constraint_column_usage AS col_constraints
                                                        ON tab_columns.table_name = col_constraints.table_name AND
                                                        tab_columns.column_name = col_constraints.column_name
                                                        LEFT OUTER JOIN
                                                        information_schema.table_constraints AS tab_constraints
                                                        ON tab_constraints.constraint_name = col_constraints.constraint_name
                                                        LEFT OUTER JOIN
                                                        information_schema.check_constraints AS col_check_constraints
                                                        ON col_check_constraints.constraint_name = tab_constraints.constraint_name
                                                        WHERE tab_columns.table_name =\'''' + sys.argv[1] + '''\'''' + '''
                                                        ORDER BY ordinal_position;'''""

            cursor.execute(create_table_query)
            rec = cursor.fetchall()

            for row in rec:
                d = collections.OrderedDict()
                d['orderId'] = row[0]
                d['Column_Name'] = row[1]
                d['dataType'] = row[2]
                d['character_maximum_length'] = row[3]
                d['numeric_precision'] = row[4]
                d['is_nullable'] = row[5]
                d['constraint_type'] = row[6]
                names_as_dict.append(d)

            return jsonify({'metaDataInfo': names_as_dict})
            #return json.dumps(names_as_dict, sort_keys=True, indent=4, separators=(',', ': '))

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
        #closing database connection.
         if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

class tgtMetaDataInfo(Resource):

    def get(self,*argv):
        names_as_dict = []
        m={}
        arg=argv
        try:
            connection = psycopg2.connect(user = "shuva",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "guru99")
            cursor = connection.cursor()
            create_table_query = ""'''SELECT ordinal_position, tab_columns.column_name, data_type, character_maximum_length,
                                                        numeric_precision, is_nullable, tab_constraints.constraint_type
                                                        FROM information_schema.columns AS tab_columns
                                                        LEFT OUTER JOIN
                                                        information_schema.constraint_column_usage AS col_constraints
                                                        ON tab_columns.table_name = col_constraints.table_name AND
                                                        tab_columns.column_name = col_constraints.column_name
                                                        LEFT OUTER JOIN
                                                        information_schema.table_constraints AS tab_constraints
                                                        ON tab_constraints.constraint_name = col_constraints.constraint_name
                                                        LEFT OUTER JOIN
                                                        information_schema.check_constraints AS col_check_constraints
                                                        ON col_check_constraints.constraint_name = tab_constraints.constraint_name
                                                        WHERE tab_columns.table_name =\'''' + sys.argv[1] + '''\'''' + '''
                                                        ORDER BY ordinal_position;'''""

            cursor.execute(create_table_query)
            rec = cursor.fetchall()
            print(type(rec))
            for row in rec:
                d = collections.OrderedDict()
                d['orderId'] = row[0]
                d['Column_Name'] = row[1]
                d['dataType'] = row[2]
                d['character_maximum_length'] = row[3]
                d['numeric_precision'] = row[4]
                d['is_nullable'] = row[5]
                d['constraint_type'] = row[6]
                names_as_dict.append(d)


            return jsonify(names_as_dict)
            #return json.dumps(names_as_dict, sort_keys=True, indent=4, separators=(',', ': '))

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
        #closing database connection.
         if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

api.add_resource(srcMetaDataInfo, '/Metadata/src/' + sys.argv[1])
api.add_resource(tgtMetaDataInfo, '/Metadata/tgt/' + sys.argv[1])

if __name__ == '__main__':
     app.run(host='0.0.0.0', debug=True,port=5000, threaded=True)