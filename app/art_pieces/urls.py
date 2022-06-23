from django.urls import path
from art_pieces import views as art_pieces_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('', tutorials_views.index, name='home'),
    path('', art_pieces_views.index.as_view(), name='home'),
    path('api/art_pieces/', art_pieces_views.portfolio_list),
    path('api/art_pieces/<int:pk>/', art_pieces_views.portfolio_detail),
    path('api/art_pieces/published/', art_pieces_views.portfolio_list_published)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)