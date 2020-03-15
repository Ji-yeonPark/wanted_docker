from flask import current_app as app
from flask_restplus import Api, fields, reqparse, Resource
from sqlalchemy import or_, and_
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
model_tag = api.model('Tag', {
    'id': fields.Integer,
    'name': fields.String,
    'language': fields.String
})
model_company_tag_map = api.model('Company_Tags_Map', {
    'tag': fields.Nested(model_tag),
    'company': fields.Nested(model_company)
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


@ns_company.route("/tag/<int:company_id>")
class CompanyTagMapView(Resource):
    """Company & Tags Map View"""

    @ns_company.doc('add tag to company')
    @ns_company.marshal_with(model_company_tag_map, 201)
    def post(self, company_id):
        """ 회사에 태그 정보 추가 """
        if not api.payload:
            return '', 404

        tag = api.payload.get('tag')  # id<int>

        if not tag:
            return '', 404

        # 회사 - 태그 추가
        new_data = Company_Tags_Map(
            tag_id=tag,
            company_id=company_id
        )
        db.session.add(new_data)
        db.session.commit()
        return new_data, 201

    @ns_company.doc('delete tag from company')
    def delete(self, company_id):
        # 회사에 태그 정보 삭제
        if not api.payload:
            return '', 404
        tag = api.payload.get('tag')  # id<int>

        if not tag:
            return '', 404

        try:
            obj = Company_Tags_Map.query.filter(
                and_(Company_Tags_Map.tag_id == tag, Company_Tags_Map.company_id == company_id)).one()
            db.session.delete(obj)
            db.session.commit()
        except:
            return 'Cannot found.', 404
        else:
            return 'Deleted', 200


@ns_tag.route("/")
class TagView(Resource):
    """Tags View"""

    @ns_tag.doc('add tag to comapny')
    @ns_tag.marshal_with(model_company_tag_map, 201)
    def get(self):
        """ 태그를 포함하는 회사 검색 """
        parser.add_argument('tag')
        args = parser.parse_args()

        # 검색어가 존재하는 경우 -> 태그 검색
        if args and args.get('tag'):
            search = f"%{args['tag']}%"  # 검색어
            results = db.session.query(Company_Tags_Map) \
                .join(Tags).filter(Tags.name.like(search)) \
                .join(Company).distinct(Company_Tags_Map.company_id).all()
            return results, 200

        # 검색어가 없는 경우 -> []
        return [], 200

    @ns_tag.doc('create tag')
    @ns_tag.expect(model_tag)
    @ns_tag.marshal_with(model_tag, 201)
    def post(self):
        """ 태그 추가 """
        if not api.payload:
            return '', 404
        name = api.payload.get('name', '')
        language = api.payload.get('language', 'KO')

        # 존재하는 태그명인지 확인
        isExist = Tags.query.filter(
            and_(Tags.name == name, Tags.language == language))

        # 존재하지 않는 경우 -> 추가
        if name and not isExist.count():
            new_tag = Tags(**api.payload)
            db.session.add(new_tag)
            db.session.commit()
            return new_tag.as_dict(), 201
        else:
            return isExist.first().as_dict(), 404
