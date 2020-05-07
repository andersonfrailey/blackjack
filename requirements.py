"""
This script builds the requirements.txt file from the environment.yml file
"""
import yaml

with open("environment.yml") as f:
    content = yaml.load(f, Loader=yaml.FullLoader)
dependencies = "\n".join(content["dependencies"])
header = """# This file is auto-generated from environment.yml, do not modify.
# See that file for comments about the need/usage of each dependency.\n
"""
with open("requirements.txt", "w") as f:
    f.write(header + dependencies)
