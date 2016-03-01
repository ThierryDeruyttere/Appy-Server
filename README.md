# appy_server


# To run server

`python manage.py runserver 0.0.0.0:8000`


# cURL command to upload file
-v flag is optional

curl -v -F 'user=userName' -F 'title=fileTitle' -F  'file=@fileNAme' http://localhost:8000/upload/
