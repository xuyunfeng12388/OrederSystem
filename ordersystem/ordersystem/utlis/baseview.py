from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseAPIView(APIView):

    @staticmethod
    def response_data(code=None, msg=None, data=None, pagination=False):
        if code == "0" and pagination:
            return Response({
                "code": code,
                "msg": msg,
                "count": data["count"],
                "data": data["results"]
            })
        elif code == "0" and not pagination:
            return Response({
                "code": code,
                "msg": msg,
                "data": data
            })
        elif code != "0":
            return Response({
                "code": code,
                "msg": msg
            })


class BaseGenericAPIView(GenericAPIView):

    @staticmethod
    def response_data(code=None, msg=None, data=None, pagination=False):
        if code == "0" and pagination:
            return Response({
                "code": code,
                "msg": msg,
                "count": data["count"],
                "data": data["results"],

            })
        elif code == "0" and not pagination:
            return Response({
                "code": code,
                "msg": msg,
                "data": data
            })
        elif code != "0":
            return Response({
                "code": code,
                "msg": msg
            })


class SpecialBaseGenericAPIView(GenericAPIView):

    @staticmethod
    def response_data(code=None, msg=None, data=None, pagination=False):
        if code == "0" and pagination:
            return Response({
                "code": code,
                "msg": msg,
                "count": data["count"],
                "data": data["results"],
                "page": data["page"],
                "pages": data["pages"],
                "pagesize": data["pagesize"],
            })
        elif code == "0" and not pagination:
            return Response({
                "code": code,
                "msg": msg,
                "data": data
            })
        elif code != "0":
            return Response({
                "code": code,
                "msg": msg
            })
