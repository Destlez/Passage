from django.core.serializers import serialize
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserSerializer, CoordinatesSerializer, LevelsSerializer, ImagesSerializer, PassagesSerializer
from .models  import User, Coordinates, Levels, Images, Passages


class CoordinatesView(viewsets.ModelViewSet):
    queryset = Coordinates.objects.all()
    serializer_class = CoordinatesSerializer

class LevelView(viewsets.ModelViewSet):
    queryset = Levels.objects.all()
    serializer_class = LevelsSerializer

class ImagesView(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PassagesView(viewsets.ModelViewSet):
    queryset = Passages.objects.all()
    serializer_class = PassagesSerializer
    Http_method_names = ['get', 'post', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email']


    def create(self, request, *args, **kwargs):
        serializer = PassagesSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': None,
                    'id': serializer.data['id'],
                }
            )

        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad Request',
                    'id': None,
                }
            )

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка подключения к базе данных',
                    'id': None,
                }
            )

    def partial_update(self, request, *args, **kwargs):
        passage = self.get_object()

        if passage.status == 'new':
            serializer = PassagesSerializer(passage, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': '1',
                        'message': 'Запись успешно изменена'
                    }
                )
            else:
                return Response(
                    {
                        'status': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    'status': '0',
                    'message': f'Отклонено! {passage.get_status_display()}'
                }
            )



