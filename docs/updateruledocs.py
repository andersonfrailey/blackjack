"""
Short script to automate updating the default rules doc
"""
import json
from jinja2 import Template
from pathlib import Path


CUR_PATH = Path(__file__).resolve().parent
TEMPLATE_PATH = Path(CUR_PATH, "default_rules_template.md")
PATHOUT = Path(CUR_PATH, "default_rules.md")

def write_page(pathout, template_path, **kwargs):
    """
    Render markdown template
    ----------
    pathout: path where the HTML file will be saved
    template_path: path for the HTML template
    Returns
    -------
    None
    """
    # read and render HTML template
    template_str = Path(template_path).open("r").read()
    template = Template(template_str)
    rendered = template.render(**kwargs)
    Path(pathout).write_text(rendered)


rules =  json.load(
    Path(CUR_PATH, "..", "py21", "rules.json").open("r")
)
parameters = []
for key in rules.keys():
    if key != "schema":
        info = rules[key]
        doc_info = {
            "rule": key,
            "description": info["description"],
            "value": info["value"],
            "notes": "N/A"
        }  # dictionary to hold documentation information
        validators = info["validators"]
        validator_type = list(validators.keys())[0]
        if validator_type == "choice":
            choices = str(validators["choice"]["choices"])[1:-1]
            doc_info["possible_vals"] = choices
        elif validator_type == "range":
            min_val = validators["range"]["min"]
            max_val = validators["range"]["max"]
            doc_info["possible_vals"] = f"{min_val}-{max_val}"
        # some parameters also have additional notes to include
        if "notes" in info:
            doc_info["notes"] = info["notes"]
        parameters.append(doc_info)

write_page(PATHOUT, TEMPLATE_PATH, parameters=parameters)
