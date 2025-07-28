from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "votes"

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get() or {}

        def formatear_fecha(timestamp):
            try:
                # Si ya viene como string con formato, lo devolvemos tal cual
                if isinstance(timestamp, str) and "a. m." in timestamp or "p. m." in timestamp:
                    return timestamp
                # Si es ISO (str) o número (int/float), lo parseamos
                dt = (
                    datetime.fromisoformat(timestamp)
                    if isinstance(timestamp, str)
                    else datetime.fromtimestamp(timestamp / 1000)
                )
                return dt.strftime("%d/%m/%Y, %-I:%M:%S %p").replace("AM", "a. m.").replace("PM", "p. m.")
            except Exception:
                return timestamp  # en caso de error, lo devolvemos sin cambios

        items = []
        if isinstance(data, dict):
            for key, value in data.items():
                timestamp = value.get("timestamp")
                value["timestamp"] = formatear_fecha(timestamp)
                items.append({"id": key, **value})

        return Response(items, status=status.HTTP_200_OK)

    def post(self, request):
        ref = db.reference(self.collection_name)
        new_entry = request.data.copy()

        now = datetime.now()

        hour_12 = now.strftime("%I").lstrip("0") or "12"  
        am_pm = now.strftime("%p").lower() 

        # Reemplazar am/pm por a. m. / p. m.
        am_pm_es = "a. m." if am_pm == "am" else "p. m."

        formatted_date = now.strftime(f"%d/%m/%Y, {hour_12}:%M:%S {am_pm_es}")

        new_entry["timestamp"] = formatted_date

        pushed_ref = ref.push(new_entry)

        return Response(
            {"message": "Datos guardados", "id": pushed_ref.key},
            status=status.HTTP_201_CREATED,
        )
