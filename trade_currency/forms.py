from django.forms import ModelForm
from django import forms


from django.forms import ModelChoiceField

from django.forms import widgets
from betterforms.multiform import MultiModelForm,MultiForm
from django.core.validators import MinValueValidator, MaxValueValidator
from collections import OrderedDict

from django.contrib.auth.models import User,Group
from company.models import Company,Company_Settings

from trade_currency.models import TradeCurrency,TradePairs


from django.db.models.fields import DecimalField

limit_status =(
    (0,'+ (Plus)'),
    (1,'- (Minus)')
    )

class NonscientificDecimalField(DecimalField):
    
    def value_from_object(self, obj):
        def remove_exponent(val):
            context = decimal.Context(prec=self.max_digits)
            return val.quantize(decimal.Decimal(1), context=context) if val == val.to_integral() else val.normalize(context)

        val = super(NonscientificDecimalField, self).value_from_object(obj)
        if isinstance(val, decimal.Decimal):
            return remove_exponent(val)


class TradeCurrencyForm(forms.ModelForm):
    
    class Meta:
        model= TradeCurrency
        fields=['name','symbol','currency_label','currency_symbol','currency_image','currncytype','usd_value','status','depositcontent_one','withdrawcontent_one','address','type_currncy']
        exclude=['big_image','created_on','modified_on','created_by','modified_by','deposit_status','withdraw_status',
        'deposit_content','withdraw_content','deposit_maintenance','withdraw_maintenance','deposit_alert','withdraw_alert',
        'alert_deposit','lend_status','lending_min','lend_duration','lend_loanrate','countryname','withdraw_feestype' 
        ,'depositcontent_three','depositcontent_two','withdrawcontent_two','trans_min','balance_minimum','withdraw_fees','min_deposit','max_deposi','min_withdraw','max_withdraw',]



class TradePairsForm(forms.ModelForm):
    buylimit = forms.ChoiceField(choices=limit_status,label='Last Price Limit',required=False)
    maker_fees =forms.DecimalField(initial=0,max_digits=16,decimal_places=8,required=False,label='Last Price Value (%)')
    change_price = forms.DecimalField(initial=0,max_digits=16,decimal_places=8,required=False,label='Last Price Rate Value')
    


    class Meta:
        model= TradePairs
        fields =['from_symbol','two_symbol','pair_name','pair_url','buylimit','maker_fees','change_price','last_price','referal_fees','min_amount','status']
        exclude=['created_on','modified_on','created_by','modified_by','min_price','max_price','margin_min_price','margin_max_price','margin_loan_duration','margin_loan_rate','selllimit','taker_fees','volume_price' ]




