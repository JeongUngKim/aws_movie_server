class Config :
    HOST = 'yhdb.ceypjcevkeoj.ap-northeast-2.rds.amazonaws.com'
    DATABASE = 'movie_test_db'
    DB_USER = 'movie_user'
    DB_PASSWORD = 'yh1234db'
    SALT = 'dskj29jcdn12jn'

    # JWT 관련 변수 세팅
    JWT_SECRET_KEY ='yhacdemy20230105##hello'
    # 뱅킹등 토큰을 종료할 필요가 있을시에는 TRUE
    JWT_ACCESS_TOKEN_EXPIRES = False
    PROPAGATE_EXCEPTIONS = True
    