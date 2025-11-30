from jinja2 import Template

def format_report(html, data):
    with open(html) as file:
        template = Template(file.read())
    return template.render(data = data)