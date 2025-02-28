import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@csrf_exempt  # Disable CSRF for testing; remove this in production
def rank_shops(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]  # Get the uploaded file
        
        # Save file temporarily
        file_path = default_storage.save(uploaded_file.name, uploaded_file)

        try:
            # Read CSV file using Pandas
            df = pd.read_csv('@mock_shop_feedback.csv')

            # ✅ Perform your shop ranking logic here (Example: sort by rating)
            df["rank"] = df["rating"].rank(ascending=False)  # Example ranking logic

            # Convert DataFrame to JSON response
            result = df.to_dict(orient="records")
            return JsonResponse({"status": "success", "data": result}, safe=False)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


