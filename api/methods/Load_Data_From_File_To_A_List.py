import csv
from click import File
from fastapi import UploadFile


def load_data_from_file_to_a_list(file:UploadFile= File(...)):
    try:
        name_of_file = 'copy'+file.filename
        with open(name_of_file, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    user_file_content_list =[]
    with open(name_of_file, mode ='r') as filecontent:   
       csvFile = csv.DictReader(filecontent)
       for lines in csvFile:
            user_file_content_list.append(lines)
    filecontent.close()

    return user_file_content_list
