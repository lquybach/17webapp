import logging



def resolve_user_id(cursor, name):
    cursor.execute(
        '''
        SELECT
            user_id
        FROM
            users
        WHERE
            user_name = %s
        ''',
        (name,)
    )
    ret = cursor.fetchone()
    logging.info(f'user: {ret}')
    # if not ret:
    #     raise ValueError('サンプルが見つかりません')
    return ret['user_id']