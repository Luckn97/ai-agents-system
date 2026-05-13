from reviewer.reviewer_engine import ReviewerEngine


engine = ReviewerEngine()

engine.add_finding(
    title="Unsafe MD5 Usage",
    description="MD5 is insecure for password hashing",
    severity="high",
    file_path="auth.py",
    line=12,
    code_snippet="hashlib.md5(password.encode())",
    category="security"
)

engine.add_finding(
    title="Unsafe MD5 Usage",
    description="Duplicate finding test",
    severity="high",
    file_path="auth.py",
    line=12,
    code_snippet="hashlib.md5(password.encode())",
    category="security"
)

engine.add_finding(
    title="Possible Division By Zero",
    description="len(numbers) can be zero",
    severity="medium",
    file_path="math_utils.py",
    line=22,
    code_snippet="return total / len(numbers)",
    category="bug"
)

results = engine.get_findings()

for finding in results:
    print(finding)
