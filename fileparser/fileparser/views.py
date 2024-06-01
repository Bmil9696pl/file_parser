from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from prometheus_client import Counter, Summary
import time
from .parser import process_file

FILES_PROCESSED = Counter('files_processed_total', 'Total number of files processed')
FILE_PROCESSING_TIME = Summary('file_processing_time_seconds', 'Time spent processing files')

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file part"}, status=400)
        
        file = request.FILES['file']
        try:
            start_time = time.time()
            summary = process_file(file)
            FILES_PROCESSED.inc()
            FILE_PROCESSING_TIME.observe(time.time() - start_time)
            return JsonResponse(summary)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)