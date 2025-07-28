from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})

class DemoRestApi(APIView):

    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({"error": "Faltan campos obligatorios: name y email"}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({"message": "Item creado correctamente.", "data": data}, status=status.HTTP_201_CREATED)

class DemoRestApiItem(APIView):
    """
    Vista para manejar un item específico por 'id' en la URL.
    Métodos: PUT, PATCH, DELETE
    """

    def get_item(self, item_id):
        return next((item for item in data_list if item['id'] == item_id), None)

    def put(self, request, item_id):
        data = request.data

        if 'id' not in data:
            return Response({"error": "El campo 'id' es obligatorio en el cuerpo."}, status=status.HTTP_400_BAD_REQUEST)
        if data['id'] != item_id:
            return Response({"error": "El 'id' en el cuerpo debe coincidir con el id en la URL."}, status=status.HTTP_400_BAD_REQUEST)

        item = self.get_item(item_id)
        if not item:
            return Response({"error": "Item no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        item.clear()
        item.update(data)

        return Response({"message": "Item reemplazado correctamente.", "data": item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        data = request.data

        item = self.get_item(item_id)
        if not item:
            return Response({"error": "Item no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        for key, value in data.items():
            if key == 'id' and value != item_id:
                return Response({"error": "No se puede cambiar el 'id'."}, status=status.HTTP_400_BAD_REQUEST)
            item[key] = value

        return Response({"message": "Item actualizado correctamente.", "data": item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        item = self.get_item(item_id)
        if not item:
            return Response({"error": "Item no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        item['is_active'] = False

        return Response({"message": "Item eliminado (desactivado) correctamente."}, status=status.HTTP_200_OK)
