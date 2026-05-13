from reviewer.python_ast_analyzer import PythonASTAnalyzer
from reviewer.autofix_engine import AutoFixEngine


class ReviewCycle:

    def run(self, code: str):

        # -----------------------------------
        # INITIAL REVIEW
        # -----------------------------------

        analyzer = PythonASTAnalyzer(
            code=code,
            file_path="user_code.py"
        )

        initial_findings = analyzer.analyze()

        # -----------------------------------
        # AUTOFIX
        # -----------------------------------

        autofix_engine = AutoFixEngine()

        autofix_result = autofix_engine.apply_fixes(
            code
        )

        fixed_code = autofix_result[
            "fixed_code"
        ]

        fixes_applied = autofix_result[
            "fixes_applied"
        ]

        diff_output = autofix_result[
            "diff"
        ]

        # -----------------------------------
        # RE-REVIEW
        # -----------------------------------

        re_analyzer = PythonASTAnalyzer(
            code=fixed_code,
            file_path="fixed_user_code.py"
        )

        remaining_findings = re_analyzer.analyze()

        # -----------------------------------
        # RESOLVED FINDINGS
        # -----------------------------------

        resolved_findings = []

        initial_ids = {
            finding["id"]
            for finding in initial_findings
        }

        remaining_ids = {
            finding["id"]
            for finding in remaining_findings
        }

        for finding in initial_findings:

            if finding["id"] not in remaining_ids:

                resolved_findings.append(
                    finding
                )

        return {
            "initial_findings": initial_findings,
            "remaining_findings": remaining_findings,
            "resolved_findings": resolved_findings,
            "fixed_code": fixed_code,
            "fixes_applied": fixes_applied,
            "diff": diff_output
        }
