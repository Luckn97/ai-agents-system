import ast
import re

from reviewer.reviewer_engine import ReviewerEngine


class PythonASTAnalyzer(ast.NodeVisitor):

    def __init__(self, code: str, file_path: str = "user_code.py"):
        self.code = code
        self.file_path = file_path
        self.engine = ReviewerEngine()

    def analyze(self):
        tree = ast.parse(self.code)

        self.visit(tree)

        self.detect_hardcoded_secrets()

        return self.engine.get_findings()

    # -------------------------
    # HASHLIB MD5
    # -------------------------

    def visit_Call(self, node):

        # hashlib.md5(...)
        if isinstance(node.func, ast.Attribute):

            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "hashlib"
                and node.func.attr == "md5"
            ):

                self.engine.add_finding(
                    title="Unsafe MD5 Usage",
                    description="MD5 is insecure for password hashing",
                    severity="high",
                    file_path=self.file_path,
                    line=node.lineno,
                    code_snippet=ast.unparse(node),
                    category="security"
                )

        # os.system(...)
        if isinstance(node.func, ast.Attribute):

            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
                and node.func.attr == "system"
            ):

                self.engine.add_finding(
                    title="Unsafe os.system Usage",
                    description="os.system can lead to command injection",
                    severity="high",
                    file_path=self.file_path,
                    line=node.lineno,
                    code_snippet=ast.unparse(node),
                    category="security"
                )

        # open(...)
        if isinstance(node.func, ast.Name):

            if node.func.id == "open":

                self.engine.add_finding(
                    title="File Open Without Context Manager",
                    description="Use 'with open(...)' for safe file handling",
                    severity="low",
                    file_path=self.file_path,
                    line=node.lineno,
                    code_snippet=ast.unparse(node),
                    category="maintainability"
                )

        # random.randint(...)
        if isinstance(node.func, ast.Attribute):

            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "random"
                and node.func.attr == "randint"
            ):

                self.engine.add_finding(
                    title="Weak Random ID Generation",
                    description="Small random ranges can create collisions",
                    severity="medium",
                    file_path=self.file_path,
                    line=node.lineno,
                    code_snippet=ast.unparse(node),
                    category="security"
                )

        self.generic_visit(node)

    # -------------------------
    # MUTABLE DEFAULT ARGUMENTS
    # -------------------------

    def visit_FunctionDef(self, node):

        for default in node.args.defaults:

            if isinstance(default, ast.List):

                self.engine.add_finding(
                    title="Mutable Default Argument",
                    description="Mutable defaults can cause shared state bugs",
                    severity="medium",
                    file_path=self.file_path,
                    line=node.lineno,
                    code_snippet=ast.unparse(default),
                    category="bug"
                )

        self.generic_visit(node)

    # -------------------------
    # HARDCODED SECRETS
    # -------------------------

    def detect_hardcoded_secrets(self):

        patterns = [
            r'API_KEY\s*=\s*["\'].*["\']',
            r'SECRET\s*=\s*["\'].*["\']',
            r'TOKEN\s*=\s*["\'].*["\']',
            r'PASSWORD\s*=\s*["\'].*["\']'
        ]

        lines = self.code.split("\n")

        for index, line in enumerate(lines):

            for pattern in patterns:

                if re.search(pattern, line):

                    self.engine.add_finding(
                        title="Hardcoded Secret",
                        description="Sensitive secret hardcoded in source code",
                        severity="high",
                        file_path=self.file_path,
                        line=index + 1,
                        code_snippet=line.strip(),
                        category="security"
                    )
