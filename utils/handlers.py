import pymysql
import logging
import azure.functions as func



def with_db_error_handling(func_to_wrap):
    def wrapper(req: func.HttpRequest) -> func.HttpResponse:
        try:
            return func_to_wrap(req)
        except pymysql.err.OperationalError as e:
            logging.error(f'Operational error: {e}')
            return func.HttpResponse(f'Database operational error: {str(e)}', status_code=500)
        except pymysql.err.ProgrammingError as e:
            logging.error(f'Programming error: {e}')
            return func.HttpResponse(f'Database programming error: {str(e)}', status_code=500)
        except Exception as e:
            logging.error(f'Unexpected error: {e}')
            return func.HttpResponse(f'Unexpected error: {str(e)}', status_code=500)
    return wrapper
