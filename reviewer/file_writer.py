import os


class FileWriter:

    # -----------------------------------
    # WRITE SINGLE FILE
    # -----------------------------------

    def write_file(
        self,
        file_path,
        content
    ):

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

            return {

                "success": True,

                "file_path": file_path
            }

        except Exception as e:

            return {

                "success": False,

                "file_path": file_path,

                "error": str(e)
            }

    # -----------------------------------
    # BACKUP FILE
    # -----------------------------------

    def create_backup(
        self,
        file_path
    ):

        try:

            if not os.path.exists(
                file_path
            ):

                return None

            backup_path = (
                file_path + ".backup"
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as original:

                content = original.read()

            with open(
                backup_path,
                "w",
                encoding="utf-8"
            ) as backup:

                backup.write(content)

            return backup_path

        except Exception:

            return None
