"""
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import ConvoViewSet, PromptViewSet

from . import views

router = DefaultRouter()
router.register('convos/',ConvoViewSet,basename="convos")
router.register('promptinputs/', PromptViewSet,basename="prompt")
router.register("", views.ChannelViewSet, basename="channels")


urlpatterns = [
    path('', include(router.urls)),
]
"""

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConvoViewSet, PromptViewSet, ChannelViewSet, BlockNoteViewSet, KnowledgeBaseView
from channels.export import merge_json_files

router = DefaultRouter()
# Register viewsets with the router


router.register(r'blocknotes', BlockNoteViewSet, basename='blocknote')
router.register(r'convos', ConvoViewSet, basename='convos')
router.register(r'promptinputs', PromptViewSet, basename='prompt') # If this is here
router.register(r'knowledgebase', KnowledgeBaseView, basename='knowledgebase')
router.register(r'', ChannelViewSet, basename='channels')

# Define urlpatterns including the router's URLs
urlpatterns = [
    path('xyz/', merge_json_files),
    # then the below is not needed
    # so remove one
    # also viewsets are not supposed to be registered like this#
    # path('convos/<int:pk>/prompts/',PromptViewSet.as_view({'get': 'list'}), name='convo-prompts-list'),
    # path('convos/<int:pk>/prompts/create/', PromptViewSet.as_view({'post': 'create'}), name='create-prompt'),
    # path('prompts/<int:pk>/update/', PromptViewSet.as_view({'patch': 'update'}), name='update-prompt'),
    # path('prompts/<int:pk>/delete/', PromptViewSet.as_view({'delete': 'destroy'}), name='delete-prompt'),

]
urlpatterns += router.urls