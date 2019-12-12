"""Financial_knowledge_map_FinancialvisualizationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import relation_view
from django.conf.urls import url
from . import index_view, index_Begin_to_identify
#
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index_view.index),#实体识别 1
    path('search_entity', relation_view.search_entity),
    url(r"Begin_to_identify", index_Begin_to_identify.Begin_to_identify),
    url(r'^search_relation',relation_view.search_relation),#关系查询，很深 1
]
