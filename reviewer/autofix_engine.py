import re


class AutoFixEngine:

    def apply_fixes(self, code: str):

        fixes_applied = []

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

            fixed = original.replace("=[]", "=None")

            updated_code = updated_code.replace(
                original,
                fixed
            )

            fixes_applied.append(
                "Replaced mutable default argument with None"
            )

        # -----------------------------------
        # FIX 3 - open() Hinweis
        # -----------------------------------

        if "open(" in updated_code:

            fixes_applied.append(
                "Detected open() usage - manual context manager review recommended"
            )

        # -----------------------------------
        # FIX 4 - os.system Hinweis
        # -----------------------------------

        if "os.system(" in updated_code:

            fixes_applied.append(
                "Detected os.system() - consider subprocess.run()"
            )

        return {
            "fixed_code": updated_code,
            "fixes_applied": fixes_applied
        }
