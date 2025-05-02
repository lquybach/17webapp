from utils.db import get_db_connection
import logging



def resolve_sample_id(cursor, name):
    cursor.execute(
        '''
        SELECT
            sample_id
        FROM
            samples
        WHERE
            sample_name = %s
        ''',
        (name,)
    )
    ret = cursor.fetchone()
    logging.info(f'sample: {ret}')
    # if not ret:
    #     raise ValueError('サンプルが見つかりません')
    return ret['sample_id']
#yasudesu
