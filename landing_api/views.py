from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "formularios_landing"

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get() or {}
        items = list(data.values()) if isinstance(data, dict) else []
        return Response(items, status=status.HTTP_200_OK)

    def post(self, request):
        ref = db.reference(self.collection_name)
        new_entry = request.data.copy()

        # Obtener fecha y hora actual
        now = datetime.now()

        # Formatear la fecha según "dd/mm/yyyy, hh:mm:ss a. m./p. m." en español
        hour_12 = now.strftime("%I").lstrip("0") or "12"  # Quitar cero inicial o poner 12
        am_pm = now.strftime("%p").lower()  # am o pm en minúsculas

        # Reemplazar am/pm por a. m. / p. m.
        am_pm_es = "a. m." if am_pm == "am" else "p. m."

        formatted_date = now.strftime(f"%d/%m/%Y, {hour_12}:%M:%S {am_pm_es}")

        new_entry["timestamp"] = formatted_date

        pushed_ref = ref.push(new_entry)

        return Response(
            {"message": "Datos guardados", "id": pushed_ref.key},
            status=status.HTTP_201_CREATED,
        )
