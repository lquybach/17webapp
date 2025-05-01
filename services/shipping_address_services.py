import logging



def resolve_shipping_address_code(cursor, name):
    cursor.execute(
        '''
        SELECT
            shipping_address_code
        FROM
            shipping_addresses
        WHERE
            address_name = %s
        ''',
        (name,)
    )
    ret = cursor.fetchone()
    logging.info(f'addr: {ret}')
    # if not ret:
    #     raise ValueError('サンプルが見つかりません')
    return ret['shipping_address_code']