import os
import datetime
import logging
from functools import wraps
from flask import request, jsonify, make_response
from lib.model import User
import hashlib
import jwt


def init_logging(loggername, level=logging.INFO):
    logging.basicConfig(
        format='%(asctime)s-%(levelname)s[%(filename)s:%(lineno)s:%(funcName)s()] %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
    )
    logger = logging.getLogger(loggername)
    logger.setLevel(level)

    return logger


logger = init_logging(__name__)


def required_params(required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                _json = request.get_json()
            except Exception as ex:
                response = {
                    "status": "error",
                    "error": {"message": "Request body is missing."}}
                return make_response(jsonify(response), 400)
            err_res = {}
            missing = [r for r in required.keys() if r not in _json]
            if missing:
                for items in missing:
                    err_res[items] = "is a required field."

            wrong_types = [r for r in list(required.keys() - err_res.keys()) if not isinstance(_json[r], required[r])]
            if wrong_types:
                for items in wrong_types:
                    err_res[items] = "format is invalid."
            if err_res:
                response = {
                    "status": "error",
                    "error": err_res
                }
                return make_response(jsonify(response), 400)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def validate_password(hashed_pass, password):
    return hashed_pass == hash_password(password)


def get_user(username, session):
    return session.query(User).filter_by(username=username).first()


def validate_user_login(user, req_data):
    if user is None:
        return make_response(jsonify({"status": "error",
                                      "error": {
                                          "message": "Incorrect username"}
                                      }), 400)

    if not user.is_active:
        return make_response(jsonify({"status": "error",
                                      "error": {
                                          "message": f"{user.username} is inactive"}
                                      }), 400)

    if not validate_password(user.password, req_data["password"]):
        return make_response(jsonify({"status": "error",
                                      "error": {
                                          "message": "Incorrect credentials"}
                                      }), 400)


def create_access_token(user, secret_key):

    logger.info(f"==========> create_access_token <==========, {user._asdict()}, secrety_key: {secret_key}")
    token = jwt.encode({
        "username": user.username,
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, secret_key, algorithm="HS256")
    return token


def login_user(req_data, session):
    user = get_user(req_data["username"], session)
    val_resp = validate_user_login(user, req_data)
    if val_resp:
        return val_resp
    access_token = create_access_token(user, os.environ.get("secret_key"))

    logger.info(f"==========> token <========== {access_token}")

    return make_response(jsonify({"status": "success",
                                  "data": {
                                      "access_token": access_token,
                                      "user_name": user.username
                                  }}), 200)


def validate_request(req_data):
    token_err = validate_token(req_data)
    if token_err:
        return token_err


def validate_token(req_data):
    token = None
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
        try:
            token = authorization.split(" ")[-1]
        except:
            pass
    if token is None:
        return make_response(jsonify({"status": "error",
                                      "error": {"message": "Bearer token is missing"}}), 401)
    try:
        decoded_token = jwt.decode(token, os.environ.get('secret_key'), algorithms=['HS256'])

        logger.info(f"==========> decoded_token <========== {decoded_token}")
        req_data['user_id'] = decoded_token['user_id']

    except jwt.exceptions.ExpiredSignatureError:
        return make_response(jsonify({"status": "error",
                                      "error": {"message": "session expired, please login"}}), 401)

    except jwt.exceptions.InvalidTokenError:
        return make_response(jsonify({"status": "error",
                                      "error": {"message": "Bearer token is invalid"}}), 401)


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
