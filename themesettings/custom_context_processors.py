from company.models import Company
from django.contrib.auth.models import User,Group
from django.db.models import Q

from trade_admin_auth.models import MenuModule, MenuPermission, SubMenuModule, SubMenuPermission


def comp_profile(request):
    try:
        
        comp = Company.objects.get(id=1)

        host_url = "{0}://{1}".format(request.scheme, request.get_host())
        return {'comp_profile_name': comp.name,
                'comp_profile_id': comp.id,
                'company_fav' : comp.company_fav,
                'comp_company_logo' : comp.company_logo,
                'host_url':host_url,
                'copy_right':comp.copy_right,
                'comp_email':comp.email,
                'comp_phonenumber':comp.phone1,
                'comp_telegram':comp.telegram,
                'comp_instagram':comp.instagram,
                'comp_fb':comp.fb,
                'comp_twitter':comp.twitter,
                'comp_linkedin':comp.linkedin,
                'comp_address':comp.address1,
                'comp_city':comp.city,
                'comp_state':comp.state,
                'comp_site':comp.website
            }
    except Company.DoesNotExist:
        return {
                'comp_profile_name': 'foo',
                'company_fav' : 'leaf',
                'comp_company_logo' : None,
                'comp_favicon' : None,
                'host_url':None,
                'copy_right':None,
                'comp_email':None,
                'comp_phonenumber':None,
                'comp_instagram':None,
                'comp_telegram':None,
                'comp_fb':None,
                'comp_twitter':None,
                'comp_linkedin':None,
                }



def user_menupermissions(request):
    
    if (request.user.id):
        try:
            check_user = User.objects.get(Q(id = request.user.id) & (Q(admin_user_profile__role=0) | Q(admin_user_profile__role=1)))
            try:

            # trade admin auth menu's start

                menu_modules_manage_user = MenuModule.objects.get(module_name = 'Rate Master')
                menu_perm_manage_user = MenuPermission.objects.get(Q(access_modules_id=menu_modules_manage_user.id) & Q(user_permissions=request.user.id))

                menu_modules_sub_adm = MenuModule.objects.get(module_name = 'Manage Sub Admin')
                menu_perm_sub_adm = MenuPermission.objects.get(Q(access_modules_id=menu_modules_sub_adm.id) & Q(user_permissions=request.user.id))

                menu_module_front_page = MenuModule.objects.get(module_name = 'Master')
                menu_perm_front_page = MenuPermission.objects.get(Q(access_modules_id=menu_module_front_page.id) & Q(user_permissions=request.user.id))
                print(menu_perm_front_page.access_status,'menu_perm_front_page.access_status---------------')
                menu_module_transaction = MenuModule.objects.get(module_name = 'Gold Master')
                menu_perm_transaction = MenuPermission.objects.get(Q(access_modules_id=menu_module_transaction.id) & Q(user_permissions=request.user.id))

                menu_modules_plan = MenuModule.objects.get(module_name = 'Admin User Master')
                menu_perm_plan = MenuPermission.objects.get(Q(access_modules_id=menu_modules_plan.id) & Q(user_permissions=request.user.id))

                menu_modules_referral = MenuModule.objects.get(module_name = 'Reports')
                menu_perm_referral = MenuPermission.objects.get(Q(access_modules_id=menu_modules_referral.id) & Q(user_permissions=request.user.id))
                
                return {
                    'menu_permissions_context_manage_user':menu_perm_manage_user.access_status,
                    'menu_permissions_context_manage_sub_adm':menu_perm_sub_adm.access_status,
                    'menu_permissions_context_frontpage':menu_perm_front_page.access_status,
                    'menu_permissions_context_transaction':menu_perm_transaction.access_status,
                    'menu_permissions_context_plan':menu_perm_plan.access_status,
                    'menu_permissions_context_referral':menu_perm_referral.access_status,
                }
            except MenuPermission.DoesNotExist:
                return{
                    "menu_modules_manage_user" : None,
                    "menu_perm_manage_user" : None,
                    "menu_modules_sub_adm" : None,
                    "menu_perm_sub_adm" : None,
                    "menu_module_front_page" : None,
                    "menu_perm_front_page" : None,
                    "menu_module_transaction" : None,
                    "menu_perm_transaction" : None,
                    "menu_modules_plan" : None,
                    "menu_perm_plan" : None,
                    "menu_modules_referral" : None,
                    "menu_perm_referral" : None,



                }

        except User.DoesNotExist:
            return{
                "check_user" : None
            }
    else:

        return{}
    

def user_submenu_permissions(request):
    if (request.user.id):
        try:
            check_user = User.objects.get(Q(id = request.user.id) & (Q(admin_user_profile__role=0) | Q(admin_user_profile__role=1)))
            try:
                sub_module_userlist = SubMenuModule.objects.get(sub_module_name = 'User Master')
                sub_menu_perm_user_list = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_userlist.id) & Q(user_permissions=request.user.id))

                sub_module_adduser = SubMenuModule.objects.get(sub_module_name = 'Scheme Master')
                sub_menu_perm_adduser = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_adduser.id) & Q(user_permissions=request.user.id))

                sub_module_walletaddress = SubMenuModule.objects.get(sub_module_name = 'Scheme Amount Master')
                sub_menu_perm_walletaddress = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_walletaddress.id) & Q(user_permissions=request.user.id))

                sub_module_ticket_category = SubMenuModule.objects.get(sub_module_name = 'Company Masters')
                sub_menu_perm_ticket_category = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_ticket_category.id) & Q(user_permissions=request.user.id))

                sub_module_ticket_request = SubMenuModule.objects.get(sub_module_name = 'Customer Ledger')
                sub_menu_perm_ticket_request = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_ticket_request.id) & Q(user_permissions=request.user.id))

                sub_module_ticket = SubMenuModule.objects.get(sub_module_name = 'Scheme Wise Report')
                sub_menu_perm_ticket = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_module_ticket.id) & Q(user_permissions=request.user.id))

                sub_ticket_request = SubMenuModule.objects.get(sub_module_name = 'Rate Wise Report')
                sub_menu_ticket_request = SubMenuPermission.objects.get(Q(sub_menu_name_id = sub_ticket_request.id) & Q(user_permissions=request.user.id))

                return{
                    "sub_menu_permissions_context_userlist" : sub_menu_perm_user_list.access_status,
                    "sub_menu_permissions_context_adduser" : sub_menu_perm_adduser.access_status,
                    "sub_menu_permissions_context_walletaddress" : sub_menu_perm_walletaddress.access_status,
                    "sub_menu_permissions_context_ticket_category" : sub_menu_perm_ticket_category.access_status,
                    "sub_menu_permissions_context_ticket_request" : sub_menu_perm_ticket_request.access_status,
                    "sub_menu_permissions_ticket_request" : sub_menu_perm_ticket.access_status,
                    "sub_menu_permissions_context_request" : sub_menu_ticket_request.access_status

                                                                    

                }
            except:
                return{
                    "sub_module_userlist" : 0,
                    "sub_menu_perm_user_list" : 0,
                    "sub_module_adduser" : 0,
                    "sub_menu_perm_adduser" : 0,
                    "sub_module_walletaddress" :0,
                    "sub_menu_perm_walletaddress" :0,
                    "sub_module_ticket_category" : 0,
                    "sub_menu_perm_ticket_category" : 0,
                    "sub_module_ticket_request" : 0,
                    "sub_menu_perm_ticket_request" : 0,
                    "sub_module_ticket":0,
                    "sub_menu_perm_ticket":0,
                    "sub_ticket_request":0,
                    "sub_menu_ticket_request":0

                }
        except User.DoesNotExist:
            return{}
    else:

        return{}