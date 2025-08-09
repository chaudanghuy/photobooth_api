# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import os

# @csrf_exempt  # CSRF 토큰 무시 (API 테스트 용도로만 사용, 프로덕션에서는 보안을 강화해야 함)
# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file', None)
#         if file:
#             file_path = os.path.join('uploads', file.name)
#             with open(file_path, 'wb') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)

#             return JsonResponse({'status': 'success', 'message': 'File has been uploaded successfully.'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'No file provided.'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        if file:
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)  # uploads 디렉터리가 없으면 생성
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return JsonResponse({'status': 'success', 'message': 'File has been uploaded successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No file provided.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
