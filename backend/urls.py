"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from store import urls as store_urls
from device import urls as device_urls
from frame import urls as frame_urls
from background import urls as background_urls
from layout import urls as layout_urls
from filter import urls as filter_urls
from sticker import urls as sticker_urls
from payment import urls as payment_urls
from revenue import urls as revenue_urls
from dashboard import urls as dashboard_urls
from account import urls as account_urls
from zalopay import urls as zalopay_urls
from redeem import urls as redeem_urls
from upload import urls as upload_urls
from get_photo import urls as get_photo_urls
from django.conf import settings
from django.conf.urls.static import static
from get_photo.views import serve_photo, serve_photo_, download,serve_script, PhotoListView, PhotoDetailView, PhotoDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stores/', include(store_urls)),
    path('devices/', include(device_urls)),
    path('frames/', include(frame_urls)),
    path('backgrounds/', include(background_urls)),
    path('layouts/', include(layout_urls)),
    path('filters/', include(filter_urls)),
    path('stickers/', include(sticker_urls)),
    path('payments/', include(payment_urls)),
    path('revenues/', include(revenue_urls)),
    path('', include(dashboard_urls)),
    path('account/', include(account_urls)),
    path('zalopay/', include(zalopay_urls)),
    path('redeem/', include(redeem_urls)),
    path('upload/', include(upload_urls)),  # upload 앱의 URL을 include
    path('get_photo/', include(get_photo_urls)),  # upload 앱의 URL을 include
    path('download_photo/uploads/<path:file_path>', serve_photo, name='serve_photo'),
    path('get_photo/uploads/<path:file_path>', serve_photo_, name='serve_photo_'),
    path('download/',download),
    path('download/script.js', serve_script, name='serve_script'),
    path('photo_list', PhotoListView.as_view(), name='photo_list'),
    path('photo_detail/<str:folder_id>', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo_delete/<str:folder_id>/<str:image>', PhotoDeleteView.as_view(), name='photo_delete'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
