from flask import request
from flask_restplus import fields, Namespace, Resource as RestplusResource

from operations_api.app import db, oidc  # noqa
from operations_api.database.models import FormInstance
from operations_api.utils.logging import ClassLoggerMixin
from operations_api.v1.modelform.utils import FormTemplateCollector

api = Namespace('modelform', description='Model Form related operations')

forminstance = api.model('FormInstance', {
    'id': fields.String,
    'template': fields.String
})


class Resource(ClassLoggerMixin, RestplusResource):
    pass


@api.route('/template')
@api.doc(headers={
    'Authorization': 'Bearer {access_token}'
})
class TemplateList(Resource):

    @oidc.accept_token(require_token=True)
    @api.marshal_list_with(forminstance)
    def get(self):
        """
        Get all stored form templates.
        """
        _list = FormInstance.query.all()
        self.logger.debug('objects: {}, count: {}'.format(_list, len(_list)))
        return FormInstance.query.all(), 200

    @oidc.accept_token(require_token=True)
    @api.marshal_with(forminstance)
    @api.doc(params={
        'version': 'Form template version (optional)'
    })
    def post(self):
        """
        Generate new form template.
        """
        ftc = FormTemplateCollector()
        version = None
        if 'version' in request.args:
            versions = ftc.list_versions()
            if not request.args['version'] in versions:
                msg = 'Invalid version, valid versions are: {}'.format(', '.join(versions))
                api.abort(400, msg)
            version = request.args.get('version')
        instance = FormInstance(template=ftc.render(version))
        db.session.add(instance)
        db.session.commit()
        self.logger.debug('object: {}'.format(instance))
        return instance, 200


@api.route('/template/<string:uuid>')
@api.doc(headers={
    'Authorization': 'Bearer {access_token}'
})
class Template(Resource):

    @oidc.accept_token(require_token=True)
    @api.marshal_with(forminstance)
    def get(self, uuid):
        """
        Get form template by UUID.
        """
        instance = FormInstance.query.get(uuid)
        self.logger.debug('object: {}'.format(instance))
        return instance, 200


@api.route('/versions')
class Versions(Resource):

    @oidc.accept_token(require_token=True)
    def get(self):
        """
        Get all available form versions.
        """
        ftc = FormTemplateCollector()
        versions = ftc.list_versions()
        self.logger.debug('object: {}'.format(versions))
        return {'versions': versions}, 200
