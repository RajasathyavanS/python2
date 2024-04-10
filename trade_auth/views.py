from django.shortcuts import render
from django.shortcuts import render,get_list_or_404, get_object_or_404
from django.conf import settings


from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView,FormView
from django.views.generic import TemplateView,View

from django.contrib.auth import login, logout, authenticate
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.urls import reverse_lazy
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.http import JsonResponse

from datetime import date,timedelta
import datetime


from datetime import date, timedelta
import decimal
from decimal import *
from django.db.models import Q,F,Func,Value
from django.db.models import Count, Min,Max, Sum, Avg,DecimalField,DateTimeField,CharField
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast,TruncSecond,ExtractSecond


from django.db import transaction

from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template import RequestContext

from trade_perms.mixins import OR_PermissionsRequiredMixin, shared_permission_access, admin_permission_access
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required,user_passes_test
from django.core.exceptions import PermissionDenied
from auditable.views import AuditableMixin

from django.contrib.auth import update_session_auth_hash

from django.core import serializers


from django_ajax.decorators import ajax


from django_tables2 import RequestConfig


import requests
import json
import urllib


import random
from random import randint

from django.template.loader import get_template
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from trade_referal.models import UserGenerationLevel
from trade_admin_auth.mixins import get_client_ip,get_browser_type,get_browser_os_type,get_browser_device_type
from django.template import loader

from company.models import Company,Company_Settings

import uuid
import pyotp
from functools import wraps
import csv
from io import StringIO
from itertools import groupby
from dateutil.relativedelta import relativedelta
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import base64
import re
from Crypto.Cipher import AES

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import base64, json, math

from themesettings.views import check_attempt,accountlocked,check_company,offline_view,home

def trade_log_out(request):
    user_id = request.user.id
    if user_id:
        tradeuser_activity_history(request,request.user.id,typelogin='Logout')
        auth.logout(request)
    else:
        auth.logout(request)
    return HttpResponseRedirect('/',)