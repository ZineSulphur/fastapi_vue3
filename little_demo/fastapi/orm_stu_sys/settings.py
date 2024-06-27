TORTOISE_ORM={
        'connections':{# 数据库连接配置
            'default':{
                'engine':'tortoise.backends.mysql', #mysql
                # 'engine':'tortoise.backends.asyncpg', #pg
                'credentials':{
                    'host':'127.0.0.1',
                    'port':'3306',
                    'user':'root',
                    'password':'root',
                    'database':'fastapi_learn',
                    'minsize':1,
                    'maxsize':5,
                    'charset':'utf8mb4',
                    'echo':True
                }
            }
        },
        'apps':{
            'models':{
                'models':['models','aerich.models',], # 加载模组类，aerich迁移还需要加'aerich.models'
                'default_connection':'default' 
            }
        },
        'use_tz':False,
        'timezone':'Asia/Shanghai'
    }