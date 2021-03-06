"""
Django settings for wjproject_v1 project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!4bbttnj60=*3qllh+9r#^kg=rk65p$2v2amhpwavlk#7)^oq+'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# ALLOWED_HOSTS = ['*', ] 	# 允许所有的IP可以访问

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', '39.105.175.144',
                 "www.genghenggao.top", "genghenggao.top"]

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # myapp
    'corsheaders',
    'channels',
    'rest_framework',
    'rest_framework_mongoengine',
    'rest_framework.authtoken',
    'wjproject_app',
    'wjproject_users',

]


REST_FRAMEWORK = {
    # DEFAULT_PERMISSION_CLASSES设置默认的权限类，通过认证后赋予用户的权限
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # 进行token认证
    )
}


SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=2),  # 访问令牌的有效时间
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),  # 访问令牌的有效时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # 刷新令牌的有效时间

    'ROTATE_REFRESH_TOKENS': False,     # 若为True，则刷新后新的refresh_token有更新的有效时间
    'BLACKLIST_AFTER_ROTATION': True,   # 若为True，刷新后的token将添加到黑名单中,
                                        # When True,'rest_framework_simplejwt.token_blacklist',should add to INSTALLED_APPS

    'ALGORITHM': 'HS256',       # 对称算法：HS256 HS384 HS512  非对称算法：RSA
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,      # if signing_key, verifying_key will be ignore.
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),           # Authorization: Bearer <token>
    # if HTTP_X_ACCESS_TOKEN, X_ACCESS_TOKEN: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',                      # 使用唯一不变的数据库字段,将包含在生成的令牌中以标识用户
    'USER_ID_CLAIM': 'user_id',

    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),   # default: access
    # 'TOKEN_TYPE_CLAIM': 'token_type',         # 用于存储令牌唯一标识符的声明名称 value:'access','sliding','refresh'
    #
    # 'JTI_CLAIM': 'jti',
    #
    # 'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',     # 滑动令牌是既包含到期声明又包含刷新到期声明的令牌
    # 'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),       # 只要滑动令牌的到期声明中的时间戳未通过，就可以用来证明身份验证
    # 'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # path('token|refresh', TokenObtainSlidingView.as_view())
}

# 以下 wjproject_users为我创建的app文件夹名称， UserInfoModel为wjproject_users下的models.py中的用户表名称
# AUTH_USER_MODEL = 'wjproject_users.UserInfoModel'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 设置可跨域
    'corsheaders.middleware.CorsMiddleware',# 注册组件cors
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # 发送post报403
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# WEBSOCKET_ACCEPT_ALL = True  # 可以允许每一个单独的视图实用websockets
CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 指定ASGI的路由地址
ASGI_APPLICATION = 'wjproject_v1.asgi.application'


ROOT_URLCONF = 'wjproject_v1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['wjproject_ui/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wjproject_v1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 设置默认数据库，这里用来存放用户信息
    # mongoengine模块目前还不支持Django ORM
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'djongo',
        'NAME': 'userInfo',
        'CLIENT': {
            'host': '127.0.0.1:27017',
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Add for vuejs
STATICFILES_DIRS = [  # 添加静态文件路径
    # os.path.join(BASE_DIR, "wjproject_ui/dist"),
    os.path.join(BASE_DIR, "wjproject_ui/dist/static"),
]
# 设置收集静态资源的路径(部署时使用)
# STATIC_ROOT ='static' #这里已经是在虚拟环境目录下了
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATIC_ROOT ='/usr/local/wjproject_docker/wjproject_env/wjproject_ui/dist/static'

# #  配置文件路径
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 使用自己local_settings.py
try:
    from .local_settings import *
except ImportError:
    pass
