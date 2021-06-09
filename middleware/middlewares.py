from django.db import connection


class QueryCountDebugMiddleware(object):
    """Debug query count - use for DEBUG only."""
    """
    This middleware will log the number of queries run
    and the total time taken for each request (with a
    status code of 200). It does not currently support
    multi-db setups.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        total_time = 0

        for query in connection.queries:
            query_time = query.get('time')
            print(str(query))

            if query_time is None:
                query_time = query.get('duration', 0) / 1000
            total_time += float(query_time)

        print('%s queries run, total %s seconds' % (len(connection.queries), total_time))
        # response["Access-Control-Allow-Origin"] = "http://10.1.2.213:3000/"
        # response["Access-Control-Allow-Headers"] = "*"
        return response