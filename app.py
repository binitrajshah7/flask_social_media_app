import pytz
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource
from flask_cors import CORS
from sqlalchemy.engine.row import Row
from lib.model import get_session_class
from lib.utils import init_logging, required_params, login_user, validate_request
from lib.service_controllers import create_map, search_map, update_map

logger = init_logging(__name__)
load_dotenv()

app = Flask('social_media_app')
CORS(app, resources={r"/*": {"origins": ["*"]}})
Session, _ = get_session_class(os.environ.get("db_uri"))

api = Api(app, version='1.0', title='Ripplr VTS APIs',
          description='CRUD APIs for Ripplr VTS')
ns = api.namespace('api/v1', description='VTS API Operations')


@app.route('/health-check', methods=["GET"])
def ping():
    logger.info(f"==========> health-check <==========")
    return jsonify({"status": "ok"})


@ns.route("/login", methods=["POST"])
class Login(Resource):
    @required_params({"username": str, "password": str})
    def post(self):
        logger.info(f"==========> login <==========")
        req_data = request.get_json()
        try:
            with Session() as session:
                return login_user(req_data, session)
        except Exception as ex:
            return make_response(jsonify({"status": "error",
                                          "error": {
                                              "message": f"Exception occurred while login.",
                                          }}), 500)


@ns.route("/create", methods=["POST"])
class Create(Resource):
    @required_params({"create_type": str, "data": dict})
    def post(self):
        req_data = request.json
        try:
            with Session() as session:
                if req_data["create_type"] not in ["user"]:
                    val_err = validate_request(req_data)
                    if val_err:
                        return val_err
                    req_data["data"]["user_id"] = req_data["user_id"]
                ret_obj = create_map[req_data["create_type"]](req_data["data"], session)
                session.commit()
                return make_response(jsonify({"status": "success",
                                              "data": ret_obj._asdict()}), 200)
        except Exception as e:
            return make_response(jsonify({"status": "error",
                                          "error": {"message": str(e)}}), 500)


@ns.route("/update", methods=["POST"])
class Update(Resource):
    @required_params({"update_type": str, "data": dict})
    def post(self):
        req_data = request.json
        try:
            with Session() as session:
                val_err = validate_request(req_data)
                if val_err:
                    return val_err

                req_data["data"]['user_id'] = req_data["user_id"]
                ret_obj = update_map[req_data["update_type"]](req_data["data"], session)
                session.commit()
                return make_response(jsonify({"status": "success",
                                          "data": ret_obj._asdict()}), 200)
        except Exception as e:
            return make_response(jsonify({"status": "error",
                                          "error": {"message": str(e)}}), 500)


@ns.route("/search", methods=["POST"])
class Search(Resource):
    @required_params({"limit": int, "offset": int})
    def post(self):
        req_data = request.json
        try:
            with Session() as session:
                val_err = validate_request(req_data)
                if val_err:
                    return val_err

                req_data["filter_by"]['user_id'] = req_data["user_id"]
                res_obj, count = search_map[req_data["search_type"]](session,
                                                                     req_data["filter_by"],
                                                                     req_data['limit'],
                                                                     req_data['offset'])

                res = []
                if res_obj is not None:
                    for row in res_obj:
                        if not isinstance(row, dict):
                            row = row._asdict() if isinstance(row, Row) else row.__dict__
                        row.pop("_sa_instance_state", None)
                        res.append(row)
                if not count:
                    count = len(res)

            res_dict = {"status": "success",
                        "data": res,
                        "meta": {"count": count}}
            return make_response(jsonify(res_dict), 200)
        except Exception as e:
            return make_response(jsonify({"status": "error",
                                          "error": {"message": str(e)}}), 500)



if __name__ == "__main__":
    app.run(debug=True, port=5001)
