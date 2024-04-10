from django.urls import include, path,re_path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
app_name = 'trade_admin_auth'

from . import views
from .views import EditCompanySetting,editprofilesetting,ChangePasswordView
from .views import ListSubAdmin,CreateSubadminUser,DeleteSubAdmin,ListAdminactivity
from .views import DetailTradeUser
from .views import ChangePatternView,EditSubadmin,ListTradeDeactiveUserAdmin,ListUseractivity
from .views import DeleteTwoFAAdmin,ListTradeUserAdmin,DeleteTradeuserAdmin,ListTwoFAUserAdmin
from .views import ListAttemptIPBlock,DeleteAttemptIPBlock,ListBlockIp,AddBlockIp,EditBlockIp,schememaster
from .views import Admin_passwordresetconfirm
#from .views import ListUserAddress,WalletDetail
from django.views.decorators.csrf import csrf_exempt

app_name = 'trade_admin_auth'

loginurl='/W8n9cQU3MAh1mjhT/'

urlpatterns = [

	 re_path('admin_auth', views.adminlogin_auth, name='admin_auth'),
	 re_path('logout',    login_required(views.log_out,login_url=loginurl), name='logout'),
	 re_path('dashboard',    login_required(views.dashboard,login_url=loginurl), name='dashboard'),
	 re_path('adminforgotpassword', views.adminforgotpassword, name='adminforgotpassword'),
	 re_path(r'^admin_confirm_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.Admin_passwordresetconfirm,name='admin_confirm_reset'),
	 re_path('adminforgotpattern', views.adminforgotpattern, name='adminforgotpattern'),
	 re_path(r'^adminpatternupdate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.Adminpatternupdate, name='adminpatternupdate'),
	 re_path(r'^general_settings/(?P<pk>[-\w]+)/$', login_required(views.EditCompanySetting.as_view(),login_url=loginurl), name='general_settings'),
	 re_path(r'^profile_settings/(?P<user_id>[-\w]+)/$', login_required(views.editprofilesetting,login_url=loginurl), name='profile_settings'),
	 re_path(r'^change_password/$', login_required(ChangePasswordView.as_view(),login_url=loginurl), name='change_password'),
	 re_path(r'^patternchange/(?P<user_id>[-\w]+)/$', login_required(views.change_pattern_view,login_url=loginurl), name='patternchange'),
	 re_path(r'^subadminactivity/$', login_required(ListAdminactivity.as_view(),login_url=loginurl), name='subadminactivity'),

	 re_path(r'^sub_admin_profile_settings/(?P<user_id>[-\w]+)/$', login_required(views.edit_subadmin_profilesetting,login_url=loginurl), name='sub_admin_profile_settings'),
	 re_path('subadminlist',    login_required(ListSubAdmin.as_view(),login_url=loginurl), name='subadminlist'),
	 re_path(r'^updatepermissions/(?P<user_id>[-\w]+)/$',  login_required(views.SubAdmin_FormView,login_url=loginurl), name='updatepermissions'),
	 re_path('subadmin_add',    login_required(CreateSubadminUser.as_view(),login_url=loginurl), name='subadmin_add'),
	 path('subadmin_sub_menu_add/<int:id>/',views.CreateSubAdmin_SubMenu_User,name = "subadmin_sub_menu_add"),
	 re_path(r'^delete_subadmin/(?P<pk>[-\w]+)/$', login_required(DeleteSubAdmin.as_view(),login_url=loginurl), name='delete_subadmin'),
	 re_path(r'^edit_subadmin/(?P<pk>[-\w]+)/$', login_required(views.EditSubadmin.as_view(),login_url=loginurl), name='edit_subadmin'),
     re_path(r'^subadmin_change_password/(?P<user_id>[-\w]+)/$', csrf_exempt(views.SubAdminChangePasswordView), name='subadmin_change_password'),
     re_path(r'^subadmin_patternchange/(?P<user_id>[-\w]+)/$', login_required(views.sub_adminchange_pattern_view,login_url=loginurl), name='subadmin_patternchange'),
	 re_path(r'^subadmin_edit_permission/(?P<user_id>[-\w]+)/$', login_required(views.SubadminEditPermission,login_url=loginurl), name='subadmin_edit_permission'),
     re_path(r'^subadmin_submenu_edit_permission/(?P<user_id>[-\w]+)/$', login_required(views.Subadmin_SubMenu_EditPermission,login_url=loginurl), name='subadmin_submenu_edit_permission'),
	 
	 re_path(r'^2fauserdelete/(?P<pk>[-\w]+)/$', login_required(DeleteTwoFAAdmin.as_view(),login_url=loginurl), name='2fauserdelete'),
	 re_path('tradeuserlist', login_required(ListTradeUserAdmin.as_view(),login_url=loginurl), name='tradeuserlist'),
	 re_path('deactivateuserlist', login_required(ListTradeDeactiveUserAdmin.as_view(),login_url=loginurl), name='deactivateuserlist'),
	 re_path(r'^delete_tradeuser/(?P<pk>[-\w]+)/$', login_required(DeleteTradeuserAdmin.as_view(),login_url=loginurl), name='delete_tradeuser'),
	 re_path('twofalist', login_required(ListTwoFAUserAdmin.as_view(),login_url=loginurl), name='twofalist'),
	 re_path(r'^detail_tradeuser/(?P<pk>[-\w]+)/$', login_required(DetailTradeUser.as_view(),login_url=loginurl), name='detail_tradeuser'),
	 re_path('activityuserlist', login_required(ListUseractivity.as_view(),login_url=loginurl), name='activityuserlist'),
	 re_path('admin2fa', login_required(views.admintwofaupdate,login_url=loginurl), name='admin2fa'),
	 re_path(r'^twofaadmin/(?P<uid>[-\w]+)', views.admintwofa, name='twofaadmin'),
	 re_path('attemptiplist', login_required(ListAttemptIPBlock.as_view(),login_url=loginurl), name='attemptiplist'),
	 re_path(r'^attempt_deleteblockip/(?P<pk>[-\w]+)/$', login_required(DeleteAttemptIPBlock.as_view(),login_url=loginurl), name='attempt_deleteblockip'),
	
	 re_path('blockiplist', login_required(ListBlockIp.as_view(),login_url=loginurl), name='blockiplist'),
	 re_path('addblockip', login_required(AddBlockIp.as_view(),login_url=loginurl), name='addblockip'),
	 re_path(r'^editblockip/(?P<pk>[-\w]+)/$', login_required(views.EditBlockIp.as_view(),login_url=loginurl), name='editblokip'),

	 #re_path(r'^useraddresslist/$', login_required(ListUserAddress.as_view(),login_url=loginurl), name='useraddresslist'),
	 #re_path(r'^walletdetail/(?P<pk>[-\w]+)/$', login_required(WalletDetail.as_view(),login_url=loginurl), name='walletdetail'),

	 
	 re_path(r'^page_403', views.Page403View, name='page_403'),
	 re_path(r'^page_404', views.Page404View, name='page_404'),
	 re_path(r'^page_500', views.Page500View, name='page_500'),
	 re_path(r'^ipblock404', views.IPBlock404View, name='ipblock404'),
	 re_path(r'^ipblockadmin', views.blockipadmin, name='ipblockadmin'),
	 re_path(r'^adminblockip404', views.adminblockip404, name='adminblockip404'),
     
	 re_path('scheme_master',  login_required(schememaster.as_view(),login_url=loginurl), name='scheme_master'),
	path('getschemedetails/', csrf_exempt(views.getschemedetails),name = "getschemedetails"),
	 re_path('amout_mast', login_required(views.amout_mast,login_url=loginurl), name='amout_mast'),
	path('getschemeamount/', csrf_exempt(views.getschemeamount),name = "getschemeamount"),
	 re_path('gold_mast', login_required(views.gold_mast,login_url=loginurl), name='gold_mast'),
	path('getschemegold/', csrf_exempt(views.getschemegold),name = "getschemegold"),
     
    
     
    
    


	


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)