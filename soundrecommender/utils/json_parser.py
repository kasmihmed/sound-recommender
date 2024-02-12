import json
from django.http.request import HttpRequest
from playlists.exceptions import JsonParsingError


def get_data_from_request_body(request: HttpRequest):
    try:
        data = json.loads(request.body)["data"]
        if type(data) is not list:
            raise JsonParsingError(
                f"could not parse the following as json {request.body}"
            )
        return data
    except:
        raise JsonParsingError(f"could not parse the following as json {request.body}")
