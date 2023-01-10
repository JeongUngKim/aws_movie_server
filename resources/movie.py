from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from mysql.connector import Error

from flask_jwt_extended import get_jwt_identity

from mysql_connection import get_connection

class MovieListResource(Resource) :
    @jwt_required(optional=True)
    def get(self) :
        user_id = get_jwt_identity()
        print('유저 ID')
        print(user_id)

        if user_id is None :
            print('비회원 유저가 접속함')
        else :
            print('회원이 접속함')

        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            if user_id is None :
                
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
            else :
                query = '''select m.id, m.title, 
                        ifnull(count(r.movie_id), 0) as cnt , 
                        ifnull(avg(r.rating) , 0)  as avg,
                        if(f.id is not null , 1, 0) as 'favorite'
                        from movie m 
                        left join rating r
                        on m.id = r.movie_id
                        left join favorite f 
                        on m.id = f.movie_id and f.user_id = %s
                        group by m.id
                        order by '''+ order +''' desc
                        limit '''+ offset +''' , '''+ limit +''' ;'''

                record = (user_id,)
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query,record)

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

class MovieResource(Resource) :
    @jwt_required(optional=True)
    def get(self,movie_id) :
        
        try :
            connection = get_connection()
            query = '''select m.* , ifnull(count(r.id),0) as cnt , 
			ifnull(avg(r.rating),0) as avg
            from movie m
            left join rating r
            on m.id = r.movie_id
            where m.id = %s;'''
            record = (movie_id,)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            result_list = cursor.fetchall()
            
            if result_list[0]['id'] is None :
                return {'result' : 'fail' , 'error' : '존재하지 않습니다.'},400     
            
            i = 0
            for row in result_list :
                result_list[i]['avg'] = float( row['avg'] )
                result_list[i]['year'] = result_list[i]['year'].isoformat()
                i = i + 1
            cursor.close()
            connection.close()
        except Error as e :
            cursor.close()
            connection.close()
            return {'result':'fail','error':str(e)},500
        


        return {'result':'success','movie':result_list[0]},200

class MovieReviewResource(Resource) :
    def get(self,movie_id) :
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        try :
            connection = get_connection()
            query = '''select r.id, u.name,u.gender, r.rating
                        from rating r
                        join user u 
                        on r.user_id = u.id
                        where r.movie_id = %s
                        limit '''+offset+''' , '''+limit + ''';'''
            record = (movie_id,)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            result_list = cursor.fetchall()
            
            if result_list[0]['id'] is None :
                return {'result' : 'fail' , 'error' : '존재하지 않습니다.'},400     
            
            cursor.close()
            connection.close()
        except Error as e :
            cursor.close()
            connection.close()
            return {'result':'fail','error':str(e)},500
        


        return {'result':'success','movie':result_list},200
        
        


