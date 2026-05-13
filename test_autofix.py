from reviewer.autofix_engine import AutoFixEngine


code = """
import hashlib

def create_user(name, password, roles=[]):

    hashed = hashlib.md5(password.encode()).hexdigest()

    return hashed
"""

engine = AutoFixEngine()

result = engine.apply_fixes(code)

print("FIXES APPLIED:")
print("------------------")

for fix in result["fixes_applied"]:
    print(f"- {fix}")

print("\nUPDATED CODE:")
print("------------------")
print(result["fixed_code"])
