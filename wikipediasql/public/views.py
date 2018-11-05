# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, abort
from flask_paginate import Pagination, get_page_parameter
import sqlalchemy
from sqlalchemy.sql import text
from time import time
from ..extensions import db

blueprint = Blueprint('public', __name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


@blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return render_template('home.html', error=True, error_message=error.message), error.status_code


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


def _to_utf8(row):
    def _helper(column):
        if type(column) == bytes:
            return column.decode("utf-8")
        else: 
            return column
    return map(_helper, row)


def _execute_query(query, fetch_size=10, **kwargs):
    try:
        tic = time()
        result = db.engine.execute(query, kwargs)
        toc = time()
        return result.keys(), list(map(_to_utf8, result.fetchmany(fetch_size))), toc - tic
    except sqlalchemy.exc.ProgrammingError:
        raise InvalidUsage("Invalid query, check your syntax", status_code=400)
    except sqlalchemy.exc.OperationalError:
        raise InvalidUsage("You are note allowed to perform that operation", status_code=401)
    except:
        abort(500)
    
    

# sqlalchemy.exc.OperationalError
# sqlalchemy.exc.ProgrammingError
@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    headers = {}
    rows = []
    execution_time = 0
    pagination = None
    if request.method == 'POST':
        query_input= request.form.get('query', '')
        headers, rows, execution_time = _execute_query(text(query_input))
        page = request.args.get(get_page_parameter(), type=int, default=1)
        pagination = Pagination(page=page, per_page=5, total=len(rows), css_framework='bootstrap4')
    return render_template("home.html", keys=headers, result=rows, execution_time="%.2fs" % execution_time, pagination=pagination)

@blueprint.route('/outdated', methods=['GET', 'POST'])
def outdated():
    """Outdated page."""
    headers = {}
    rows = []
    execution_time = 0
    if request.method == 'POST':
        query = text(
        "SELECT a.page_id, cast(a.page_title as CHAR) title, a.page_touched as referrerDate, b.page_touched as referredDate"
        " FROM (select * from page where page_id in (select cl_from from categorylinks where lower(cast(cl_to as CHAR)) = :category)) as a"
            " JOIN"
            " pagelinks as p on a.page_id = p.pl_from"
            " JOIN"
            " page as b on p.pl_title = b.page_title and b.page_touched > a.page_touched"
        " ORDER BY (b.page_touched - a.page_touched) desc"
        " LIMIT 1;")
        category_input =request.form.get('category', '').replace(' ', '_').lower()
        headers, rows, execution_time = _execute_query(query, category=category_input)
        post = True
    return render_template("outdated.html", keys=headers, result=rows, execution_time="%.2fs" % execution_time)
