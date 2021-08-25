'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-07-05 09:46:12
LastEditors: henggao
LastEditTime: 2021-08-24 14:22:02
'''
"""
ASGI config for wjproject_v1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from wjproject_app.urls import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wjproject_v1.settings')

# application = get_asgi_application() #原始的

application = ProtocolTypeRouter({
    # Explicitly set 'http' key using Django's ASGI application.
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
 