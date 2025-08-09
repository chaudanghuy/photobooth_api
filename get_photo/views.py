from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import quote
import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime

def serve_script(request):
    script_file_path = os.path.join(settings.BASE_DIR, 'get_photo/templates', 'script.js')
    print(script_file_path) 
    try:
        with open(script_file_path, 'r', encoding='utf-8') as file:
            script_content = file.read()
        return HttpResponse(script_content, content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)
from django.conf import settings

def download(request):
    image_path = request.GET.get('image_path', '')
    video_path = request.GET.get('video_path', '')
    uuid = request.GET.get('uuid', '')

    try:
       if uuid == '':
            html_file_path = os.path.join(settings.BASE_DIR, 'get_photo', 'templates', 'download.html')
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                # {{ image_path }}와 {{ video_path }}를 실제 값으로 대체
                html_content = html_content.replace('{{ image_path }}', image_path)
                html_content = html_content.replace('{{ video_path }}', video_path)
            return HttpResponse(html_content)
       else:        
            upload_dir = os.path.join(settings.BASE_DIR, 'uploads', uuid)            
            image_urls = [image_path]
            for filename in os.listdir(upload_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_file = os.path.join(request.build_absolute_uri().split("?")[0].replace("\\","/"), upload_dir.replace("\\","/"), filename)
                    image_urls.append(f'/get_photo/uploads/{image_file}')
            
            context = {        
                'image_path': image_path,
                'video_path': video_path,
                'image_urls': image_urls
            }        

            return render(request, 'download2.html', context)
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)

class PhotoListView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):        
        uploads_dir = os.path.join(settings.BASE_DIR, 'uploads')
        subfolders = []
        for f in os.scandir(uploads_dir):
            if f.is_dir():
                folder_path = os.path.join(uploads_dir, f.name)
                date_created = datetime.fromtimestamp(os.path.getctime(folder_path))
                subfolders.append({'name': f.name, 'date_created': date_created})
        
        subfolders = sorted(subfolders, key=lambda x: x['date_created'], reverse=True)
        return render(request, 'photo_list.html', {'subfolders': subfolders})

class PhotoDetailView(LoginRequiredMixin, View):

    def get(self, request, folder_id, *args, **kwargs):
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads', folder_id)
        images = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        images_view_url = []
        for image in images:
            image_url = os.path.join(request.build_absolute_uri().split("?")[0].replace("\\","/"), upload_dir.replace("\\","/"), image);
            images_view_url.append({
                'url': f'/get_photo/uploads/{image_url}',
                'name': image
            })

        return render(request, 'photo_detail.html', {'folder_id': folder_id, 'images': images_view_url})

class PhotoDeleteView(LoginRequiredMixin, View):

    def post(self, request, folder_id, image, *args, **kwargs):

        if request.method == 'POST':
            try:
                image_path = os.path.join(settings.BASE_DIR, 'uploads', folder_id, image)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    return redirect('photo_detail', folder_id=folder_id)
                else:
                    return HttpResponse('Image not found', status=404)
            except Exception as e:
                return HttpResponse('Image not found', status=404)


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        uuid = request.POST.get('uuid', None)
        if file and uuid:
            # 파일 확장자 확인
            _, file_extension = os.path.splitext(file.name)
            
            # MP4 파일인 경우 video 폴더에 저장
            if file_extension.lower() == '.mp4':
                upload_dir = os.path.join('uploads', uuid, 'video')
            else:
                upload_dir = os.path.join('uploads', uuid)
            
            # 디렉터리가 없다면 생성
            os.makedirs(upload_dir, exist_ok=True)
            
            # 파일 경로 조합
            file_path = os.path.join(upload_dir, file.name)
            
            # 파일 저장
            try:
                with open(file_path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return JsonResponse({'status': 'success', 'message': 'File has been uploaded successfully.'})
            except IOError as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'No file or UUID provided.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def get_photos(request):
    if request.method == 'GET':
        uuid = request.GET.get('uuid', None)
        print('uploads',uuid)
        upload_dir = os.path.join('uploads',uuid.split("uploads/")[-1].replace("\\","/"))
        video_dir = os.path.join(upload_dir, 'video')
        print("###########")
        print("upload_dir")
        print(upload_dir)
        print("###########")
        try:
            # 이미지 파일 처리
            file_list = os.listdir(upload_dir)
            images = [file for file in file_list if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            images.sort()
            image_urls = [{'id': idx, 'url': os.path.join(request.build_absolute_uri().split("?")[0].replace("\\","/"), upload_dir.replace("\\","/"), image.replace("\\","/"))} for idx, image in enumerate(images)]
            
            # 비디오 파일 처리
            video_list = os.listdir(video_dir) if os.path.exists(video_dir) else []
            videos = [file for file in video_list if file.lower().endswith('.mp4')]
            videos.sort()
            video_urls = [{'id': idx, 'url': os.path.join(request.build_absolute_uri().split("?")[0].replace("\\","/"), video_dir.replace("\\","/"), video.replace("\\","/"))} for idx, video in enumerate(videos)]
            
            print("###########")
            print("image_urls")
            print(image_urls)
            print("video_urls")
            print(video_urls)
            print("###########")
            
            return JsonResponse({'status': 'success', 'images': image_urls, 'videos': video_urls})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

#@csrf_exempt
#def serve_photo(request, file_path):
#    base_path = file_path.replace("\\", "/")
#    full_path = os.path.join('uploads', base_path)

#    logger.info(f"Requested file path: {full_path}")

    # MP4 파일에 대한 특별 처리
#    if full_path.lower().endswith('.mp4'):
        # UUID 부분을 추출
#        path_parts = full_path.split(os.path.sep)
#        uuid_index = path_parts.index('uploads') + 1 if 'uploads' in path_parts else 0
#        if uuid_index < len(path_parts) - 1:
#            uuid = path_parts[uuid_index]
#            filename = path_parts[-1]
#            full_path = os.path.join('uploads', uuid, 'video', filename)
#            logger.info(f"Adjusted MP4 file path: {full_path}")

#    if os.path.exists(full_path):
#        with open(full_path, 'rb') as f:
#            content_type = "video/mp4" if full_path.lower().endswith('.mp4') else "image/jpeg"
#            response = HttpResponse(f.read(), content_type=content_type)
#            response['Content-Disposition'] = f'inline; filename={quote(os.path.basename(full_path))}'
#            return response
#    else:
#        #logger.error(f"File not found: {full_path}")
#        raise Http404("File not found")

import os
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import logging
import mimetypes

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def serve_photo(request, file_path):
    if request.method == "OPTIONS":
        return handle_options_request()

    base_path = file_path.replace("\\", "/")
    full_path = os.path.join('uploads', base_path)

    logger.info(f"Requested file path: {full_path}")

    if not os.path.exists(full_path):
        logger.error(f"File not found: {full_path}")
        return HttpResponse(status=404)

    try:
        content_type, _ = mimetypes.guess_type(full_path)
        if not content_type:
            content_type = 'application/octet-stream'

        response = FileResponse(open(full_path, 'rb'), content_type=content_type)
        
        # 모든 파일을 다운로드하도록 설정
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(full_path)}"'

        # 파일 크기 설정
        response['Content-Length'] = os.path.getsize(full_path)
        
        # CORS 헤더 추가
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

        logger.info(f"Serving file: {full_path}")
        logger.info(f"Content type: {content_type}")
        logger.info(f"File size: {os.path.getsize(full_path)} bytes")

        return response
    except IOError as e:
        logger.exception(f"IOError while serving file: {full_path}")
        return HttpResponse(f"Error reading file: {str(e)}", status=500)
    except Exception as e:
        logger.exception(f"Unexpected error while serving file: {full_path}")
        return HttpResponse(f"Unexpected error: {str(e)}", status=500)

def handle_options_request():
    response = HttpResponse()
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response



from django.http import HttpResponse, Http404
from urllib.parse import quote

@csrf_exempt
def serve_photo_(request, file_path):
    file_path = os.path.join('uploads', file_path.replace("\\","/"))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="image/jpeg")
            response['Content-Disposition'] = f'inline; filename={quote(os.path.basename(file_path))}'
            return response
    else:
        raise Http404("File not found")



@csrf_exempt
def delete_photo(request, folder_id, image):
    if request.method == 'GET':
        try:
            upload_dir = os.path.join(settings.BASE_DIR, 'uploads', folder_id)
            file_path = os.path.join(upload_dir, image)
            os.remove(file_path)                        
            return JsonResponse({'status': 'success', 'message': 'File has been deleted successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


















































#@csrf_exempt
#def serve_photo(request, file_path):
#    base_path = os.path.join('uploads', file_path.replace("\\","/"))
#    if file_path.lower().endswith('.mp4'):
#        file_path = os.path.join(base_path, 'video', os.path.basename(file_path))
#    else:
#        file_path = base_path
#
#    if os.path.exists(file_path):
#        with open(file_path, 'rb') as f:
#            content_type = "video/mp4" if file_path.lower().endswith('.mp4') else "image/jpeg"
#            response = HttpResponse(f.read(), content_type=content_type)
#            response['Content-Disposition'] = f'inline; filename={quote(os.path.basename(file_path))}'
#            return response
#    else:
#        raise Http404("File not found")
