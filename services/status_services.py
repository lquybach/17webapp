import logging



def resolve_status_no(cursor, name):
    cursor.execute(
        '''
        SELECT
            status_no
        FROM
            statuses
        WHERE
            status_name = %s
        ''',
        (name,)
    )
    ret = cursor.fetchone()
    logging.info(f'status: {ret}')
    return ret['status_no']