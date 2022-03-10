import re
from os import listdir
from os.path import isfile, join
from utils.upload import upload


def upload_files(session, node_id, dir_path, file_identifier=""):
    """
    Uploads the files stored in a specific dir
    to alfresco

    Parameters:
        session (Session):          A session object to make
                                    requests to alfresco.
        node_id (string):           Node id to which the file is going to be created
        dir_path (string):          The name and path of the dir where files are stored
        file_identifier (string):   File identifier for all files inside a dir

    Returns:
        (string):           Returns the info of recent created site.
    """

    files_in_dir = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    try:
        
        files_uploaded = []
        for idx,file in enumerate(files_in_dir):

            data = {
                "name": (
                    file[0 : len(file) - 4]
                    + file_identifier
                    + file[len(file) - 4 : len(file)]
                ),
                "nodeType": "cm:content",
            }

            is_allowed_type = False

            if re.search(".(gif|jpg|jpeg|tiff|png)", file.lower()):
                data["relativePath"] = "Fotos"
                is_allowed_type = True
            elif re.search(".(wav)", file.lower()):
                data["relativePath"] = "Audios"
                is_allowed_type = True
            elif re.search(".(avi)", file.lower()):
                data["relativePath"] = "Videos"
                is_allowed_type = True

            if is_allowed_type:

                data["properties"] = {
                    "cm:title": (
                        file[0 : len(file) - 4]
                        + file_identifier
                        + file[len(file) - 4 : len(file)]
                    )
                }

                status_code = None
                repeat = 0

                print("Uploading " + data["name"] + " file...")

                while status_code != 201:

                    files = {"filedata": open(dir_path + "/" + file, "rb")}

                    upload_response = upload(session, node_id, data, files)

                    if upload_response[1] and upload_response[1] == 201:
                        files_uploaded.append(upload_response[0])

                        print("Uploaded " + data["name"])

                        status_code = upload_response[1]

                    if upload_response[1] and upload_response[1] == 409:
                        if "already exists" in upload_response[0]["error"]["errorKey"]:
                            repeat += 1
                            data["name"] = (
                                file[0 : len(file) - 4]
                                + file_identifier
                                + "_"
                                + str(repeat)
                                + file[len(file) - 4 : len(file)]
                            )
                            data["properties"] = {
                                "cm:title": (
                                    file[0 : len(file) - 4]
                                    + file_identifier
                                    + "_"
                                    + str(repeat)
                                    + file[len(file) - 4 : len(file)]
                                )
                            }
                        status_code = upload_response[1]
                print("Uploaded file " + str(idx + 1) + " of " + str(len(files_in_dir)))

        return files_uploaded
    except Exception as e:
        print("An error ocurred in file upload: ", e)
