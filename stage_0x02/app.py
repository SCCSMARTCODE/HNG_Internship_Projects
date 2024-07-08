from flask import request, jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import uuid
from __init__ import app
from model.user_model import UserModel
from model.organisation_model import OrganisationModel
from model.user_to_organisation_model import UserToOrganisationModel
from functions import token_required

from model.engine import session

session = session()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = []

    for field in ['firstName', 'lastName', 'email', 'password']:
        if not data.get(field):
            errors.append({'field': field, 'message': 'must not be null'})
        elif field == 'email':
            # checking if email exists
            email = session.query(UserModel).filter_by(email=data.get('email')).first()
            if email:
                errors.append({'field': field, 'message': 'must be unique'})
    if errors:
        return jsonify({'errors': errors}), 422

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = UserModel(userId=str(uuid.uuid4()), firstName=data['firstName'], lastName=data['lastName'],
                         email=data['email'], password=hashed_password, phone=data.get('phone'))
    session.add(new_user)
    session.commit()

    new_org = OrganisationModel(orgId=str(uuid.uuid4()), name=f"{data['firstName']}'s Organisation", description="")
    session.add(new_org)
    session.commit()

    user_org = UserToOrganisationModel(userId=new_user.userId, orgId=new_org.orgId, isCreator=True)
    session.add(user_org)
    session.commit()

    token = jwt.encode({'user_id': new_user.userId, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=48)},
                       app.config['SECRET_KEY'])
    return jsonify({'status': 'success', 'message': 'Registration successful',
                    'data': {'accessToken': token, 'user': new_user.to_dict()}}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = session.query(UserModel).filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'status': 'Bad request', 'message': 'Authentication failed', 'statusCode': 401}), 401

    token = jwt.encode({'user_id': user.userId, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                       app.config['SECRET_KEY'])
    return jsonify({'status': 'success', 'message': 'Login successful',
                    'data': {'accessToken': token, 'user': user.to_dict()}}), 200


@app.route('/api/users/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    if current_user.userId != user_id:
        user_organisations_requester = session.query(UserToOrganisationModel).filter_by(
            userId=current_user.userId).all()
        user_organisations_requested = session.query(UserToOrganisationModel).filter_by(userId=user_id).all()

        access = False
        for user_organisation_requester in user_organisations_requester:
            for user_organisation_requested in user_organisations_requested:
                if user_organisation_requester.orgId == user_organisation_requested.orgId:
                    access = True
                    break
            if access:
                break
        if not access:
            return jsonify({'message': 'Unauthorized access'}), 403

    user = session.query(UserModel).filter_by(userId=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({'status': 'success', 'message': 'User record fetched', 'data': user.to_dict()}), 200


@app.route('/api/organisations', methods=['GET', 'POST'])
@token_required
def get_organisations(current_user):
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('name') or type(data.get('name')) != str or type(data.get('description')) != str:
            return jsonify({"status": "Bad Request", "message": "Client error", "statusCode": 400})
        new_org = OrganisationModel(
            name=data.get('name'),
            description=data.get('description')
        )
        session.add(new_org)
        session.commit()
        new_user_to_org = UserToOrganisationModel(
            userId=current_user.userId,
            orgId=new_org.orgId
        )
        session.add(new_user_to_org)
        session.commit()
        return jsonify({
            "status": "success",
            "message": "Organisation created successfully",
            "data": new_org.to_dict()
        }), 201

    orgs_to_user = session.query(UserToOrganisationModel).filter_by(userId=current_user.userId).all()
    orgs = [session.query(OrganisationModel).filter_by(orgId=org_to_user.orgId).first() for org_to_user in orgs_to_user]

    return jsonify({'status': 'success', 'message': 'Organisations fetched',
                    'data': {'organisations': [org.to_dict() for org in orgs]}}), 200


@app.route('/api/organisations/<org_id>', methods=['GET'])
@token_required
def get_organisation(current_user, org_id):
    org_to_user = session.query(UserToOrganisationModel).filter_by(userId=current_user.userId, orgId=org_id).first()
    if not org_to_user:
        return jsonify({'message': 'Unauthorized access'}), 403
    org = session.query(OrganisationModel).filter_by(orgId=org_to_user.orgId).first()
    return jsonify({'status': 'success', 'message': 'Organisation fetched', 'data': org.to_dict()}), 200


@app.route('/api/organisations/<org_id>/users', methods=['POST'])
def add_user_to_organisation(org_id):

    data = request.get_json()
    if not data.get('userId'):
        return jsonify({"status": "Bad Request", "message": "Client error", "statusCode": 400})
    if not session.query(UserModel).filter_by(userId=data.get('userId')).first():
        return jsonify({"status": "Bad Request", "message": "Client error", "statusCode": 400})

    new_user_to_org = UserToOrganisationModel(
        userId=data.get('userId'),
        orgID=org_id
    )
    session.add(new_user_to_org)
    session.commit()
    return jsonify({
        "status": "success",
        "message": "User added to organisation successfully",
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
