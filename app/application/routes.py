from flask import current_app as app
from flask_restplus import Api, fields, reqparse, Resource
from sqlalchemy import or_
from .models import db, Company, Tags, Company_Tags_Map

api = Api(app, version='1.0', title='Wanted API',
          description='Wanted Coding Test')

# namespace
ns_company = api.namespace('company', description='Company operations')
ns_tag = api.namespace('tag', description='Tag operations')

# marshal model
model_company = api.model('Company', {
    'id': fields.Integer,
    'name_ko': fields.String,
    'name_en': fields.String,
    'name_ja': fields.String,
})

# parser
parser = reqparse.RequestParser()


# routers
@ns_company.route("/")
class CompanyView(Resource):
    """Company View"""

    @ns_company.doc('search company')
    @ns_company.marshal_with(model_company, 200)
    def get(self):
        """ 회사명 검색 - 자동완성기능 """

        parser.add_argument('name')
        args = parser.parse_args()

        # 검색어가 존제하는 경우 -> 조건 검색
        if args and args.get('name'):
            search = f"%{args['name']}%"  # %검색어%
            return Company.query.filter(or_(
                Company.name_ko.like(search),
                Company.name_en.like(search),
                Company.name_ja.like(search)
            )).distinct(Company.id).all()

        # 검색어가 없는 경우 -> 전체 검색
        return Company.query.all()
