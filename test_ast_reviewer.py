from reviewer.python_ast_analyzer import PythonASTAnalyzer


code = """
import hashlib
import random
import os

API_KEY = "123456-secret"

users = {}

def create_user(name, password, roles=[]):

    hashed = hashlib.md5(password.encode()).hexdigest()

    user_id = random.randint(1, 5)

    users[user_id] = {
        "name": name,
        "password": hashed,
        "roles": roles
    }

    return user_id


def load_file(path):

    file = open(path, "r")

    return file.read()


def run_command(cmd):

    os.system(cmd)


create_user("admin", "123456")
"""

analyzer = PythonASTAnalyzer(code)

findings = analyzer.analyze()

for finding in findings:
    print(finding)
