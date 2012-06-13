from pyramid.response import Response
from pyramid.view import view_config
import simplejson as json

from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import (
        HTTPFound,
        HTTPNotFound,
        )

from .models import (
    DBSession,
    BadCase,
    createCase,
    listAllCases,
    closeCase,
    reopenCase,
    )

@view_config(route_name='home', renderer='templates/homepage.pt')
def home_view(request):
    offset = request.params.get('offset', 0)
    limit = request.params.get('limit', 20)
    status = request.params.get('status', '')
    print "%s %s %s" % (offset, limit, status)
    cases = listAllCases(offset, limit, status)

    caseStrList = []
    for case in cases:
        caseStrList.append(str(case))

    return dict(offset=offset, limit=limit, badcases=caseStrList)

@view_config(route_name='report', renderer='templates/report.pt')
def report_view(request):
    url = request.params.get('url', '')
    desc = request.params.get('desc', '')
    if url:
        createCase(url, desc)
        return HTTPFound(location = request.route_url('home', offset=0, limit=20, status='all'))
    report_url = request.route_url('report')
    return dict(report_url=report_url)

@view_config(route_name='modify', renderer='templates/modify.pt')
def modify_view(request):
    if 'form.submitted' in request.params:
        return HTTPFound(location = request.route_url('home', offset=0, limit=20, status='all'))

    bid = request.params.get('id', 0)
    try:
        case = DBSession.query(BadCase).filter(BadCase.id==bid).first()
    except:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    modify_url = request.route_url('modify')
    return dict(case=case, modify_url=modify_url)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_badreporter_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

