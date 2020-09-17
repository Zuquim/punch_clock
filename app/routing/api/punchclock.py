from datetime import datetime as dt
from time import strftime

from flask import jsonify, make_response, request

from app import db
from app.models import PunchClock, User
from app.routing import headers, row2dict
from app.routing.api import api_bp, api_log as log


def success_reply_dict(action: str, request: request, punch_obj: PunchClock) -> dict:
    return {
        "datetime": strftime("%Y-%m-%d %H:%M:%S"),
        "from": request.remote_addr,
        "action": action,
        "target": f"user_id={punch_obj.user.get_id()}",
        "message": f"User (id={punch_obj.user.get_id()}) punch(es) {action}d successfully",
    }


@api_bp.route("/api/get/punches/user/<int:uid>", methods=["GET"])
def list_user_punches(uid):
    """List user's punches details."""

    # Checking if user exists in DB
    user_exists = User.query.filter(User.id == uid).first()
    if not user_exists:
        error_msg = f"User (id={uid}) does not exist!"
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 205

    # Logging and returning
    user_punches = [
        row2dict(pc) for pc in PunchClock.query.filter(PunchClock.user_id == uid).all()
    ]
    reply = success_reply_dict("select", request, PunchClock.query.filter(PunchClock.user_id == uid).first())
    log.info(reply["message"])
    return jsonify(punches=user_punches)


@api_bp.route("/api/new/punch", methods=["POST"])
def new_punch():
    """Create a new punch."""

    try:
        user_id = request.json["user_id"]
        punch_type = request.json["punch_type"].lower()
        if punch_type != "in" and punch_type != "out":
            raise KeyError("'punch_type' must be either 'in' or 'out'")
    except KeyError as e:
        error_msg = (
            "JSON must contain the following attributes: user_id; punch_type(in/out);"
            f" | Missing attribute: {e}"
        )
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 400

    # Checking if user exists in DB
    user_exists = User.query.filter(
        User.id == user_id
    ).first()  # Create an instance of the User model class
    if not user_exists:
        error_msg = f"User (id={user_id}) does not exist!"
        log.error(error_msg)
        return make_response(jsonify({"message": error_msg}), headers["json"]), 400

    # Committing changes to DB
    now = dt.now()
    new_punch = PunchClock(
        user_id=user_exists.get_id(),
        user=user_exists,
        punch_type=punch_type,
        created=now,
    )  # Create an instance of the PunchClock model class
    db.session.add(new_punch)  # Adds new PunchClock record to database
    db.session.commit()  # Commits all changes

    # Logging and returning
    reply = success_reply_dict("create", request, new_punch)
    log.info(reply["message"])
    return make_response(jsonify(reply), headers["json"]), 200
