from werkzeug.datastructures import FileStorage
import config
import os
import uuid


class FileServer(object):
    def __init__(self, file_type) -> None:

        if file_type == "audio":
            self.folder = "audio"
        else:
            self.folder = None

    def save_file(self, file: FileStorage):
        try:
            if not self.folder:
                raise {
                    "error": "invalid file type"
                }

            self.file = file
            self.file_extension = file.filename.rsplit('.', 1)[1]
            filename = str(uuid.uuid4()) + "." + self.file_extension
            self.filename = filename

            path = str(os.getcwd() + f"../FILES/{self.folder}/")
            print("new file -> " ,path)
            if not os.path.exists(path):
                os.makedirs(path)
            self.file.save(os.path.join(path, filename))
            print(type(filename))
            return {
                "file": filename
            }
        except ValueError as e:
            return {
                "error": str(e)
            }



# test = file_server("audio" , 1)
