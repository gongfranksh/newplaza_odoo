import json

import datetime
from psycopg2._psycopg import Decimal


class MsSqlResultDataEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        return super(MsSqlResultDataEncoder, self).default(obj)