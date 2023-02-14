from rest_framework.response import Response

def responce_util(status, error, response):
    return Response({"status": status, "error": error, "response": response},status=status)