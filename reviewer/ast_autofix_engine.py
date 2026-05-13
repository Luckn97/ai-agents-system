import ast
import difflib


class ASTAutoFixTransformer(ast.NodeTransformer):

    def __init__(self):

        self.fixes_applied = []

        self.requires_subprocess = False
        self.requires_uuid = False
        self.requires_os = False

    # -----------------------------------
    # hashlib.md5 -> hashlib.sha256
    # -----------------------------------

    def visit_Call(self, node):

        self.generic_visit(node)

        # hashlib.md5(...)
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "hashlib"
            and node.func.attr == "md5"
        ):

            node.func.attr = "sha256"

            self.fixes_applied.append(
                "Replaced insecure MD5 with SHA256"
            )

        # os.system(...)
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr == "system"
        ):

            self.requires_subprocess = True

            node.func.value.id = "subprocess"
            node.func.attr = "run"

            node.keywords.append(
                ast.keyword(
                    arg="shell",
                    value=ast.Constant(value=True)
                )
            )

            self.fixes_applied.append(
                "Replaced os.system with subprocess.run"
            )

        # random.randint(1, 5)
        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "random"
            and node.func.attr == "randint"
        ):

            self.requires_uuid = True

            new_node = ast.Call(
                func=ast.Name(
                    id="str",
                    ctx=ast.Load()
                ),
                args=[
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(
                                id="uuid",
                                ctx=ast.Load()
                            ),
                            attr="uuid4",
                            ctx=ast.Load()
                        ),
                        args=[],
                        keywords=[]
                    )
                ],
                keywords=[]
            )

            self.fixes_applied.append(
                "Replaced weak random ID generation with uuid4"
            )

            return ast.copy_location(
                new_node,
                node
            )

        return node

    # -----------------------------------
    # Mutable Default Arguments
    # -----------------------------------

    def visit_FunctionDef(self, node):

        self.generic_visit(node)

        for i, default in enumerate(node.args.defaults):

            if isinstance(default, ast.List):

                node.args.defaults[i] = ast.Constant(
                    value=None
                )

                self.fixes_applied.append(
                    "Replaced mutable default argument with None"
                )

        return node

    # -----------------------------------
    # Hardcoded Secrets
    # -----------------------------------

    def visit_Assign(self, node):

        self.generic_visit(node)

        if (
            len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):

            variable_name = node.targets[0].id

            if (
                "KEY" in variable_name
                or "TOKEN" in variable_name
                or "SECRET" in variable_name
            ):

                self.requires_os = True

                node.value = ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(
                            id="os",
                            ctx=ast.Load()
                        ),
                        attr="getenv",
                        ctx=ast.Load()
                    ),
                    args=[
                        ast.Constant(
                            value=variable_name
                        )
                    ],
                    keywords=[]
                )

                self.fixes_applied.append(
                    f"Moved {variable_name} to environment variable"
                )

        return node


class ASTAutoFixEngine:

    def apply_fixes(self, code: str):

        original_code = code

        tree = ast.parse(code)

        transformer = ASTAutoFixTransformer()

        updated_tree = transformer.visit(tree)

        ast.fix_missing_locations(
            updated_tree
        )

        # -----------------------------------
        # IMPORT HANDLING
        # -----------------------------------

        existing_imports = []

        for node in updated_tree.body:

            if isinstance(node, ast.Import):

                for alias in node.names:

                    existing_imports.append(
                        alias.name
                    )

        new_imports = []

        if (
            transformer.requires_subprocess
            and "subprocess" not in existing_imports
        ):

            new_imports.append(
                ast.Import(
                    names=[
                        ast.alias(
                            name="subprocess"
                        )
                    ]
                )
            )

        if (
            transformer.requires_uuid
            and "uuid" not in existing_imports
        ):

            new_imports.append(
                ast.Import(
                    names=[
                        ast.alias(
                            name="uuid"
                        )
                    ]
                )
            )

        if (
            transformer.requires_os
            and "os" not in existing_imports
        ):

            new_imports.append(
                ast.Import(
                    names=[
                        ast.alias(
                            name="os"
                        )
                    ]
                )
            )

        updated_tree.body = (
            new_imports
            + updated_tree.body
        )

        # -----------------------------------
        # GENERATE CODE
        # -----------------------------------

        fixed_code = ast.unparse(
            updated_tree
        )

        # -----------------------------------
        # DIFF
        # -----------------------------------

        diff = difflib.unified_diff(
            original_code.splitlines(),
            fixed_code.splitlines(),
            fromfile="original.py",
            tofile="fixed.py",
            lineterm=""
        )

        diff_output = "\n".join(diff)

        return {

            "fixed_code": fixed_code,

            "fixes_applied": list(
                set(transformer.fixes_applied)
            ),

            "diff": diff_output
        }
