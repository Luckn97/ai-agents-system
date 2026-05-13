import os


class ProjectLoader:

    def __init__(self):

        self.supported_extensions = [
            ".py"
        ]

    # -----------------------------------
    # FIND FILES
    # -----------------------------------

    def load_project(self, project_path):

        project_files = []

        for root, dirs, files in os.walk(
            project_path
        ):

            # -----------------------------------
            # IGNORE COMMON FOLDERS
            # -----------------------------------

            dirs[:] = [

                d for d in dirs

                if d not in [
                    "__pycache__",
                    ".git",
                    ".venv",
                    "venv",
                    "node_modules"
                ]
            ]

            # -----------------------------------
            # FIND PY FILES
            # -----------------------------------

            for file in files:

                if any(

                    file.endswith(ext)

                    for ext in self.supported_extensions
                ):

                    full_path = os.path.join(
                        root,
                        file
                    )

                    project_files.append(
                        full_path
                    )

        return project_files

    # -----------------------------------
    # READ FILE
    # -----------------------------------

    def read_file(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return file.read()

        except Exception as e:

            return (
                f"# FILE_READ_ERROR: {str(e)}"
            )

    # -----------------------------------
    # LOAD FULL PROJECT
    # -----------------------------------

    def load_project_files(
        self,
        project_path
    ):

        files = self.load_project(
            project_path
        )

        loaded_files = []

        for file_path in files:

            content = self.read_file(
                file_path
            )

            loaded_files.append({

                "file_path": file_path,

                "content": content
            })

        return loaded_files
