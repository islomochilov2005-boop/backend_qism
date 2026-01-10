from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    @staticmethod
    def success(data=None, message="Muvaffaqiyatli", status_code=status.HTTP_200_OK):
        return Response({
            'success': True,
            'message': message,
            'data': data
        }, status=status_code)

    @staticmethod
    def error(message="Xatolik yuz berdi", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            'success': False,
            'message': message,
            'errors': errors
        }, status=status_code)

    @staticmethod
    def created(data=None, message="Yaratildi"):
        return Response({
            'success': True,
            'message': message,
            'data': data
        }, status=status.HTTP_201_CREATED)


# apps/core/pagination.py - Yangi fayl
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })