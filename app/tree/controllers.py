# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, Response
from app.api.models import dm_dict_en, Urls
from app import db
from app.tree.mk_urls_file import make_csv_pod, make_png_pod
import requests


# Define the blueprint:
tree = Blueprint('tree', __name__, url_prefix='/my-tree')

@tree.route('/')
@tree.route('/index', methods=['GET','POST'])
def index():
    query = db.session.query(Urls.keyword.distinct().label("keyword"))
    keywords = [row.keyword for row in query.all()]
    print(keywords)
    pears = []
    for keyword in keywords:
         if keyword:
             pear_urls = []
             for u in db.session.query(Urls).filter_by(keyword=keyword).all():
                 pear_urls.append(u)
             pear = [keyword, len(pear_urls)]
             pears.append(pear)
    #for p in sorted(pears, key=lambda p: len(pears[p]), reverse=True):
    #    print(p,len(pears[p]),pears[p][:5])
    return render_template('tree/index.html',pears=pears)

@tree.route('/get-a-pod', methods=['POST','GET'])
def get_a_pod():
    query = request.args.get('pod')
    csv_location = make_csv_pod(query)
    png_locations = make_png_pod(query)
    print(png_locations)
    return render_template('tree/get-a-pod.html',query=query,csv_location=csv_location,png_locations=png_locations)
