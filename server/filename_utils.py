def get_extension(filename: str) -> str:
    return filename.rsplit('.', 1)[1]


def is_filename_valid(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ["jpg", "png", "jpeg", "gif"]
