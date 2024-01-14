class FileUtil:
    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            result = file.read()
            return result
