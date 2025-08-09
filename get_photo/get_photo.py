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
def get_photos(request):
    if request.method == 'GET':
        upload_dir = os.path.join('uploads')  # 파일을 저장할 디렉터리 경로 설정
        # 디렉터리 내의 모든 파일 목록을 가져옴
        try:
            file_list = os.listdir(upload_dir)
            # 이미지 파일만 필터링 (예: JPEG, PNG 파일)
            images = [file for file in file_list if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            image_urls = [{'id': idx, 'url': os.path.join(request.build_absolute_uri(), upload_dir, image)} for idx, image in enumerate(images)]
            return JsonResponse({'status': 'success', 'images': image_urls})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
