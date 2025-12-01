from jinja2 import Template
from flask import request

def format_report(html, data):
    with open(html) as file:
        template = Template(file.read())
    return template.render(**data)


def spec_key(func=None):
    spec_id = request.args.get("id", "")
    name = request.args.get("name", "")
    return f"specialization:id={spec_id}|name={name}"

def pat_key(func=None):
    id = request.args.get("id", "")
    uid = request.args.get("uid", "")
    return f"patient:id={id}|uid={uid}"

def doc_key(func=None):
    id = request.args.get("id", "")
    uid = request.args.get("uid", "")
    return f"doctor:id={id}|uid={uid}"

def appt_key(func=None):
    appt_id = request.args.get("id", "")
    pid = request.args.get("pid", "")
    did = request.args.get("did", "")
    return f"appointment:id={appt_id}|pid={pid}|did={did}"