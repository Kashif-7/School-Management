from flask import Flask, Blueprint, jsonify

bp = Blueprint("root", __name__)

@bp.route("/")
def root():
    return("Welcome to School Management System", 200)