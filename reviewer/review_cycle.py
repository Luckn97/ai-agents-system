from reviewer.python_ast_analyzer import PythonASTAnalyzer
from reviewer.autofix_engine import AutoFixEngine


class ReviewCycle:

    def __init__(self):

        self.max_iterations = 5

    def analyze_code(self, code, file_path):

        analyzer = PythonASTAnalyzer(
            code=code,
            file_path=file_path
        )

        return analyzer.analyze()

    def run(self, code: str):

        current_code = code

        autofix_engine = AutoFixEngine()

        iteration_results = []

        # -----------------------------------
        # ITERATION LOOP
        # -----------------------------------

        for iteration in range(
            1,
            self.max_iterations + 1
        ):

            # -----------------------------------
            # REVIEW
            # -----------------------------------

            findings = self.analyze_code(
                current_code,
                f"iteration_{iteration}.py"
            )

            # -----------------------------------
            # STOP IF CLEAN
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
                f"fixed_iteration_{iteration}.py"
            )

            # -----------------------------------
            # RESOLVED
            # -----------------------------------

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

            # -----------------------------------
            # STORE ITERATION
            # -----------------------------------

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

                "diff": diff_output
            })

            # -----------------------------------
            # STOP IF NO CHANGES
            # -----------------------------------

            if fixed_code == current_code:

                break

            current_code = fixed_code

        # -----------------------------------
        # FINAL REVIEW
        # -----------------------------------

        final_findings = self.analyze_code(
            current_code,
            "final_code.py"
        )

        return {

            "iterations": iteration_results,

            "final_findings": final_findings,

            "final_code": current_code,

            "success": len(final_findings) == 0
        }
