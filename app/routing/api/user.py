from datetime import datetime as dt
from time import strftime

from flask import jsonify, make_response, request

from app import db
from app.models import User
from app.routing import headers, row2dict
from app.routing.api import api_bp, api_log as log


def success_reply_dict(action: str, request_obj: request, user_obj: User) -> dict:
    return {
        "datetime": strftime("%Y-%m-%d %H:%M:%S"),
        "from": request_obj.remote_addr,
        "action": action,
        "target": f"user_id={user_obj.get_id()}",
        "message": f"User (full_name='{user_obj.full_name}'; cpf={user_obj.cpf}; email={user_obj.email}) {action}d successfully",
    }


def validate_cpf(cpf: str):  # TODO: implement it
    """Validates a numeric string representing a CPF."""

    if len(cpf) != 11:
        return False

    if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
        return False

    calc = lambda t: int(t[1]) * (t[0] + 2)
    d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
    d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11

    return str(d1) == cpf[-2] and str(d2) == cpf[-1]


@api_bp.route("/api/get/user/<int:uid>", methods=["GET"])
def get_user(uid):
    """Get specific User details."""

    # Checking if user exists in DB
    user_exists = User.query.filter(User.id == uid).first()
    if not user_exists:
        error_msg = f"User (id={uid}) does not exist!"
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 205

    # Logging and returning
    reply = success_reply_dict("select", request, user_exists)
    log.info(reply["message"])
    return jsonify(user=row2dict(user_exists))


@api_bp.route("/api/list/users", methods=["GET"])
def list_users():
    """List users' details."""
    return jsonify(users=[row2dict(u) for u in User.query.all()]), 200


@api_bp.route("/api/new/user", methods=["POST"])
def new_user():
    """Create a new User."""

    try:
        full_name = request.json["full_name"]
        cpf = request.json["cpf"]
        email = request.json["email"].lower()
    except KeyError as e:
        error_msg = (
            f"JSON must contain the following attributes:"
            f" cpf, email, full_name | "
            f" Did not find attribute: {e}"
        )
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 400

    # Checking if user already exists in DB
    user_exists = (
        User.query.filter(User.cpf == cpf).first()
        or User.query.filter(User.email == email).first()
    )
    if user_exists:
        error_msg = f"User (full_name='{user_exists.full_name}'; cpf={user_exists.cpf}; email={user_exists.email}) already exists!"
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"])

    # Inserting new user in DB
    now = dt.now()
    make_user = User(
        cpf=cpf, email=email, full_name=full_name, created=now
    )  # Create an instance of the User model class
    db.session.add(make_user)  # Adds new User record to database
    db.session.commit()  # Commits all changes

    # Logging and returning
    reply = success_reply_dict("create", request, make_user)
    log.info(reply["message"])
    return make_response(jsonify(reply), headers["json"]), 201


@api_bp.route("/api/update/user", methods=["POST"])
def update_user():
    """Update User attributes."""

    try:
        user_id = request.json["user_id"]
    except KeyError:
        error_msg = (
            "JSON must contain the following attribute: user_id"
            " | Optionally it may also contain: cpf, email, full_name"
        )
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 400

    cpf = request.json["cpf"] if "cpf" in request.json else None
    email = request.json["email"] if "email" in request.json else None
    full_name = request.json["full_name"] if "full_name" in request.json else None

    user_exists = User.query.filter(User.id == user_id).first()
    if not user_exists:
        error_msg = f"User (id={user_id}) does not exist!"
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 205

    if cpf:
        user_exists.cpf = cpf
        log.info(f"Updated CPF for user (id={user_exists.get_id()})")

    if email:
        user_exists.email = email
        log.info(f"Updated email for user (id={user_exists.get_id()})")

    if full_name:
        user_exists.full_name = full_name
        log.info(f"Updated full_name for user (id={user_exists.get_id()})")

    # Checking if there are updates to be applied to user
    if not db.session.dirty:
        error_msg = f"Nothing to update on user (id={user_exists.get_id()})"
        log.info(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 200

    # Committing changes to DB
    db.session.commit()  # Commits all changes

    # Logging and returning
    reply = success_reply_dict("update", request, user_exists)
    log.info(reply["message"])
    return make_response(jsonify(reply), headers["json"]), 200
