import re
import difflib


class AutoFixEngine:

    def apply_fixes(self, code: str):

        fixes_applied = []

        original_code = code

        updated_code = code

        # -----------------------------------
        # FIX 1 - MD5 -> SHA256
        # -----------------------------------

        if "hashlib.md5" in updated_code:

            updated_code = updated_code.replace(
                "hashlib.md5",
                "hashlib.sha256"
            )

            fixes_applied.append(
                "Replaced insecure MD5 with SHA256"
            )

        # -----------------------------------
        # FIX 2 - Mutable Default Arguments
        # -----------------------------------

        mutable_pattern = r"(\w+)\((.*?)=\[\]\)"

        matches = re.finditer(
            mutable_pattern,
            updated_code
        )

        for match in matches:

            original = match.group(0)

            fixed = original.replace(
                "=[]",
                "=None"
            )

            updated_code = updated_code.replace(
                original,
                fixed
            )

            fixes_applied.append(
                "Replaced mutable default argument with None"
            )

        # -----------------------------------
        # FIX 3 - os.system -> subprocess.run
        # -----------------------------------

        if "os.system(" in updated_code:

            if "import subprocess" not in updated_code:

                updated_code = (
                    "import subprocess\n"
                    + updated_code
                )

            updated_code = updated_code.replace(
                "os.system(",
                "subprocess.run("
            )

            fixes_applied.append(
                "Replaced os.system with subprocess.run"
            )

        # -----------------------------------
        # FIX 4 - Hardcoded API Keys
        # -----------------------------------

        secret_pattern = r'([A-Z_]+)\s*=\s*"([^"]+)"'

        secret_matches = re.finditer(
            secret_pattern,
            updated_code
        )

        for match in secret_matches:

            variable_name = match.group(1)

            secret_value = match.group(2)

            if (
                "KEY" in variable_name
                or "TOKEN" in variable_name
                or "SECRET" in variable_name
            ):

                original = (
                    f'{variable_name} = "{secret_value}"'
                )

                fixed = (
                    f'{variable_name} = os.getenv("{variable_name}")'
                )

                if "import os" not in updated_code:

                    updated_code = (
                        "import os\n"
                        + updated_code
                    )

                updated_code = updated_code.replace(
                    original,
                    fixed
                )

                fixes_applied.append(
                    f"Moved {variable_name} to environment variable"
                )

        # -----------------------------------
        # FIX 5 - Weak Random IDs
        # -----------------------------------

        if "random.randint(1, 5)" in updated_code:

            if "import uuid" not in updated_code:

                updated_code = (
                    "import uuid\n"
                    + updated_code
                )

            updated_code = updated_code.replace(
                "random.randint(1, 5)",
                "str(uuid.uuid4())"
            )

            fixes_applied.append(
                "Replaced weak random ID generation with uuid4"
            )

        # -----------------------------------
        # FIX 6 - open() Detection
        # -----------------------------------

        if "open(" in updated_code:

            fixes_applied.append(
                "open() detected - manual conversion to context manager recommended"
            )

        # -----------------------------------
        # DIFF GENERATION
        # -----------------------------------

        diff = difflib.unified_diff(
            original_code.splitlines(),
            updated_code.splitlines(),
            fromfile="original.py",
            tofile="fixed.py",
            lineterm=""
        )

        diff_output = "\n".join(diff)

        return {

            "fixed_code": updated_code,

            "fixes_applied": fixes_applied,

            "diff": diff_output
        }
