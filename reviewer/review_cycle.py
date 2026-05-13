from reviewer.python_ast_analyzer import PythonASTAnalyzer
from reviewer.ast_autofix_engine import ASTAutoFixEngine


class ReviewCycle:

    def __init__(self):

        self.max_iterations = 5

    # -----------------------------------
    # ANALYZE
    # -----------------------------------

    def analyze_code(
        self,
        code,
        file_path
    ):

        analyzer = PythonASTAnalyzer(
            code=code,
            file_path=file_path
        )

        return analyzer.analyze()

    # -----------------------------------
    # REVIEW SINGLE FILE
    # -----------------------------------

    def review_file(
        self,
        code,
        file_path
    ):

        current_code = code

        autofix_engine = ASTAutoFixEngine()

        iteration_results = []

        # -----------------------------------
        # ITERATION LOOP
        # -----------------------------------

        for iteration in range(
            1,
            self.max_iterations + 1
        ):

            findings = self.analyze_code(
                current_code,
                file_path
            )

            # -----------------------------------
            # CLEAN
            # -----------------------------------

            if not findings:

                iteration_results.append({

                    "iteration": iteration,

                    "status": "clean",

                    "findings": [],

                    "resolved_findings": [],

                    "remaining_findings": [],

                    "fixes_applied": [],

                    "diff": ""
                })

                break

            # -----------------------------------
            # APPLY FIXES
            # -----------------------------------

            autofix_result = autofix_engine.apply_fixes(
                current_code
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

            remaining_findings = self.analyze_code(
                fixed_code,
                file_path
            )

            remaining_titles = {

                finding["title"]

                for finding in remaining_findings
            }

            resolved_findings = []

            for finding in findings:

                if (
                    finding["title"]
                    not in remaining_titles
                ):

                    resolved_findings.append(
                        finding
                    )

            iteration_results.append({

                "iteration": iteration,

                "status": (
                    "clean"
                    if not remaining_findings
                    else "needs_review"
                ),

                "findings": findings,

                "resolved_findings": resolved_findings,

                "remaining_findings": remaining_findings,

                "fixes_applied": fixes_applied,

                "diff": diff_output,

                "final_code": fixed_code
            })

            # -----------------------------------
            # STOP IF NO CHANGE
            # -----------------------------------

            if fixed_code == current_code:

                break

            current_code = fixed_code

        # -----------------------------------
        # FINAL REVIEW
        # -----------------------------------

        final_findings = self.analyze_code(
            current_code,
            file_path
        )

        return {

            "file_path": file_path,

            "iterations": iteration_results,

            "final_findings": final_findings,

            "final_code": current_code,

            "success": len(final_findings) == 0
        }
