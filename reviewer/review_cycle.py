from reviewer.python_ast_analyzer import PythonASTAnalyzer
from reviewer.autofix_engine import AutoFixEngine


class ReviewCycle:

    def __init__(self):

        self.max_iterations = 3

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

        all_resolved_findings = []

        # -----------------------------------
        # MULTI ITERATION LOOP
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
                f"user_code_iteration_{iteration}.py"
            )

            # -----------------------------------
            # STOP IF CLEAN
            # -----------------------------------

            if not findings:

                iteration_results.append({
                    "iteration": iteration,
                    "findings": [],
                    "fixes_applied": [],
                    "diff": "",
                    "status": "clean"
                })

                break

            # -----------------------------------
            # AUTOFIX
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
            # RESOLVED FINDINGS
            # -----------------------------------

            resolved_findings = []

            remaining_titles = {
                finding["title"]
                for finding in remaining_findings
            }

            for finding in findings:

                if (
                    finding["title"]
                    not in remaining_titles
                ):

                    resolved_findings.append(
                        finding
                    )

                    all_resolved_findings.append(
                        finding
                    )

            # -----------------------------------
            # STORE ITERATION
            # -----------------------------------

            iteration_results.append({

                "iteration": iteration,

                "findings": findings,

                "remaining_findings": remaining_findings,

                "resolved_findings": resolved_findings,

                "fixes_applied": fixes_applied,

                "diff": diff_output,

                "status": (
                    "clean"
                    if not remaining_findings
                    else "needs_review"
                )
            })

            # -----------------------------------
            # STOP IF NOTHING CHANGED
            # -----------------------------------

            if fixed_code == current_code:

                break

            current_code = fixed_code

        # -----------------------------------
        # FINAL ANALYSIS
        # -----------------------------------

        final_findings = self.analyze_code(
            current_code,
            "final_code.py"
        )

        return {

            "iterations": iteration_results,

            "final_code": current_code,

            "final_findings": final_findings,

            "resolved_findings": all_resolved_findings,

            "success": len(final_findings) == 0
        }
