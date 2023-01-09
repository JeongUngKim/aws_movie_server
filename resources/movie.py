from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from mysql.connector import Error

from flask_jwt_extended import get_jwt_identity

from mysql_connection import get_connection

class MovieListResource(Resource) :

    def get(self) :

        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()

            query = '''select m.id, m.title, 
                    ifnull(count(r.movie_id), 0) as cnt , 
                    ifnull(avg(r.rating) , 0)  as avg
                    from movie m 
                    left join rating r
                    on m.id = r.movie_id
                    group by m.id
                    order by '''+ order +''' desc
                    limit '''+ offset +''' , '''+ limit +''' ;'''

            # record = (user_id, )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['avg'] = float( row['avg'] )
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)            
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 500


        print(result_list)

        return {'result' : 'success',
                'items' : result_list, 
                'count' : len(result_list)}, 200


class MovieSearchResource(Resource):

    def get(self) :

        keyword = request.args.get('keyword')
        offset = request.args.get('offset')
        limit = request.args.get('limit')


        try :
            connection = get_connection()

            query = '''select m.id, m.title, 
                    ifnull(count(r.movie_id), 0) as cnt , 
                    ifnull(avg(r.rating) , 0)  as avg
                    from movie m 
                    left join rating r
                    on m.id = r.movie_id
                    where m.title like '%'''+ keyword +'''%'
                    group by m.id
                    order by m.title 
                    limit '''+offset+''', '''+limit+''' ;'''

            # record = (user_id, )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()

            i = 0
            for row in result_list :
                result_list[i]['avg'] = float( row['avg'] )
                i = i + 1

            cursor.close()
            connection.close()

        except Error as e :
            print(e)            
            cursor.close()
            connection.close()
            return {"error" : str(e)}, 500


        print(result_list)

        return {'result' : 'success',
                'items' : result_list, 
                'count' : len(result_list)}, 200


        


