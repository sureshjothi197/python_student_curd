from flask import jsonify, request, render_template_string, send_file
from flask_restplus import Resource
from marshmallow import fields
import os
import pdfkit
from student.data_access.db_models import Students
from student.data_access.schema_definitions.student_schema import StudentSchema
from student.extensions import db, ma
from student.middleware.restplus import api
from student.serializers.student_serializer import student
from student.utils.response_code import response_format
from student.services.student.service import (delete_student,
                                                      get_all_student,
                                                      get_student, post_student,
                                                      update_student)

# from student.utils.response_constants import RESPONSE_ERROR_MESSAGE
ns = api.namespace(
    'students',
    description='Operations related to students')

@ns.route('/<int:student_id>')
class studentResource(Resource):
    """Single object resource
    """

    def get(self, student_id):
        response = get_student(student_id)
        return response_format(response)

    @api.expect(student)
    def put(self, student_id):
        response = update_student(student_id, request.json)
        return response_format(response)

    def delete(self, student_id):
        response = delete_student(student_id)
        if response:
            return response_format(response)


@ns.route('/')
class StudentList(Resource):
    """Creation and get_all
    """

    def get(self):
        response = get_all_student()
        return response, 200

    @api.expect(student)
    def post(self):
        response = post_student(request.json)
        return response, 201

@ns.route('/pdf/')
class StudentListpdf(Resource):
    """get all student list in pdf format
    """
    def get(self):
        f=open("index.html", "r")
        print("================")
        contents = f.read()
        response = get_all_student()
        # name = randomString()
        name = 'sample'
        f = open(name+'.html', "a")
        f.write(render_template_string(contents, x= response))
        f.close()
        pdfkit.from_url(name+'.html', name+'.pdf')
        path = os.path.normpath(os.getcwd())+'/'+name+'.pdf'
        return send_file(path, as_attachment=True)

    
        
        
    
