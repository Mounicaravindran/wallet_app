from rest_framework.response import Response


def success_response(data):
    response_data = {
        "data": data,
        "status": "success"
    }
    return Response(data=response_data)
