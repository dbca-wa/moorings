from django import forms
from ledger.address.models import Country
from mooring import models
from mooring import utils
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Fieldset, MultiField, Div
from django.forms import Form, ModelForm, ChoiceField, FileField, CharField, Textarea, ClearableFileInput, HiddenInput, Field, RadioSelect, ModelChoiceField, Select, CheckboxInput

class BaseFormHelper(FormHelper):
    form_class = 'form-horizontal'
    label_class = 'col-xs-12 col-sm-4 col-md-3 col-lg-2'
    field_class = 'col-xs-12 col-sm-8 col-md-6 col-lg-4'


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)

VEHICLE_TYPES = (
    ('0', 'Vessel'),
#    ('1', 'Vehicle (concession)'),
#    ('2', 'Motorcycle')
)

class CancelGroupForm(forms.ModelForm):
    mooring_group = ChoiceField(choices=[],)

    class Meta:
        model = models.CancelGroup
        fields = ['name','cancel_period','mooring_group']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(CancelGroupForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['mooring_group'].choices = []
        if 'mooring_group_choices' in self.initial:
            self.fields['mooring_group'].choices = self.initial['mooring_group_choices'] 

        self.helper.form_id = 'id_cancel_group_form'
        #self.helper.attrs = {'novalidate': ''}
        #self.helper.add_input(Submit('Continue', 'Continue', css_class='btn-lg'))


class DeleteBookingPeriodOptionForm(forms.ModelForm):
    class Meta:
        model = models.BookingPeriodOption
        fields = []

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(DeleteBookingPeriodOptionForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = 'id_delet_form'
        self.helper.add_input(Submit('Delete', 'Delete', css_class='btn-lg', style='margin-top: 15px;' ))


class BookingPeriodOptionForm(forms.ModelForm):
    #mooring_group = ChoiceField(choices=[],)
    class Meta:
        model = models.BookingPeriodOption
        fields = ['period_name','option_description','small_price','medium_price','large_price','start_time','finish_time','change_group','cancel_group','caption']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(BookingPeriodOptionForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['change_group'].choices = []
        self.fields['cancel_group'].choices = []
        if 'change_group_choices'  in self.initial:
            self.fields['change_group'].choices = self.initial['change_group_choices']
        if 'cancel_group_choices'  in self.initial:
            self.fields['cancel_group'].choices = self.initial['cancel_group_choices']


        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})

        self.helper.form_id = 'id_change_group_form'
        if self.initial['action'] == 'edit':
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;' ))

class AnnualBookingPeriodOptionForm(forms.ModelForm):
    #mooring_group = ChoiceField(choices=[],)
    class Meta:
        model = models.AnnualBookingPeriodOption
        fields = ['start_time','finish_time',]

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(AnnualBookingPeriodOptionForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})
        vessel_category_pricing = HTML('{% include "mooring/dash/add_edit_annual_vessel_category.html" %}')

        self.helper.form_id = 'id_annual_booking_periods_form'
        if self.initial['action'] == 'edit':
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;' ))

        self.helper.layout = Layout('start_time','finish_time',vessel_category_pricing)

class ChangeGroupForm(forms.ModelForm):

    class Meta:
        model = models.ChangeGroup 
        fields = ['name','change_period','mooring_group']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(ChangeGroupForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['mooring_group'].choices = []
        if 'mooring_group_choices' in self.initial:
            self.fields['mooring_group'].choices = self.initial['mooring_group_choices']
        self.helper.form_id = 'id_change_group_form'
        #self.helper.attrs = {'novalidate': ''}
        #self.helper.add_input(Submit('Continue', 'Continue', css_class='btn-lg'))


class AnnualAdmissionForm(forms.ModelForm):

    first_name = forms.CharField(label="Given Name(s)", widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'required':True, 'class': "form-control"}), label="Last Name")
    postal_address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'required':True, 'class': "form-control"}), label="Postal Address Line 1")
    postal_address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'required':False, 'class': "form-control"}), label="Postal Address Line 2", required=False)
    suburb = forms.CharField(max_length=50, label="Suburb",widget=forms.TextInput(attrs={'required':True, 'class': "form-control"}))
    postcode = forms.CharField(max_length=4, label="Post Code",widget=forms.TextInput(attrs={'required':True, 'class': "form-control"}))
    state = forms.CharField(max_length=4, label="State", widget=forms.Select(attrs={'class': "form-control" }))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), to_field_name="iso_3166_1_a2", widget=forms.Select(attrs={'class': "form-control" }))
    phone = forms.CharField(widget=forms.TextInput(attrs={'required':False, 'class': "form-control"}), label="Phone", required=False)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'required':False, 'class': "form-control"}), label="Mobile", required=False)
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'required':True, 'class': "form-control"}))
    confirm_email = forms.EmailField(label ="Confirm Email", widget=forms.TextInput(attrs={'required':True, 'class': "form-control"}))

    vessel_rego = forms.CharField(label="Vessel Registration", widget=forms.TextInput(attrs={'class': "form-control"}))
    vessel_name = forms.CharField(label="Vessel Name", widget=forms.TextInput(attrs={'class': "form-control"}))
    vessel_length = forms.CharField(label="Registered Vessel Length (meters)", widget=forms.TextInput(attrs={'class': "form-control"}))

    booking_period = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control" }))
    terms = forms.BooleanField(label="I agree to the <A href=''>terms and conditions</A> (Including insurance requirements)")

    override_price_selection = forms.BooleanField(label="Override Price", widget=forms.CheckboxInput(attrs={'class': "iiform-control", 'style' : 'margin-left: 0px; position: inherit;' }), required=False) #label="<b>Override Price</b>", required=False)
    override_price = forms.CharField(max_length=10, label="Price", widget=forms.TextInput(attrs={'required':False, 'class': "form-control", 'step' : '0.01' }), required=False)
    override_reason = forms.ChoiceField(label="Reason", widget=forms.Select(attrs={'class': "form-control" }), required=False)
    override_details = forms.CharField(widget=forms.Textarea(attrs={'required':False, 'class': "form-control"}), label="Details",required=False)

    class Meta:
        model = models.BookingAnnualAdmission
        fields = []

    def clean(self):
        super(AnnualAdmissionForm, self).clean()
       
        if ('email' in self.cleaned_data):
            if 'confirm_email' in self.cleaned_data:
                if (self.cleaned_data.get('email')) != (self.cleaned_data.get('confirm_email')):
                    raise forms.ValidationError('Your email and confirm email address do not match.')#+self.cleaned_data.get('terms'))
        if len(self.cleaned_data.get('phone')) < 8 and len(self.cleaned_data.get('mobile')) < 8:
                 raise forms.ValidationError('Please provide at least one valid phone or mobile number.')

        if self.cleaned_data.get('terms') is not True:
            raise forms.ValidationError('Please check terms and conditions.')

        vessel_length = self.cleaned_data.get('vessel_length') 
        booking_period = self.cleaned_data.get('booking_period')

        response = 'error'
        if models.AnnualBookingPeriodGroup.objects.filter(id=int(booking_period)).count() > 0:
             try:
                annual_admission = utils.get_annual_admissions_pricing_info(booking_period,vessel_length)
                price = annual_admission['abpovc'].price
                response = 'success'
                if annual_admission['response'] == 'error':
                    response = 'error'
             except:
                pass
                price = "No price available"
                response = 'error'
        if response == 'error':
             raise forms.ValidationError('Sorry, no matching booking period available for your vessel size.')

        if self.cleaned_data.get('override_price_selection') is True: 
            if self.cleaned_data.get('override_reason'):
                override_reason = self.cleaned_data.get('override_reason')
                dr = models.DiscountReason.objects.filter(id=override_reason)
                if dr[0].detailRequired is True:
                    if len(self.cleaned_data.get('override_details')) > 1:
                          pass
                    else: 
                        raise forms.ValidationError('Please complete override details')
            else:
                raise forms.ValidationError('Please select an override reason') 
             
        if float(self.cleaned_data.get('vessel_length')) > float(0.01):
             vl = self.cleaned_data.get('vessel_length')
             vl_split = vl.split('.')
             if len(vl_split) > 1:
                   if len(vl_split[1]) == 2:
                       pass
                   else:
                       raise forms.ValidationError('Invalid decimal length,  please provide a valid vessel length in decimals 0.00.')
             else:
                 raise forms.ValidationError('Please provide a valid vessel length in decimals 0.00.')
        else:
            raise forms.ValidationError('Please provide a valid vessel length.')


    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(AnnualAdmissionForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = 'id_annual_admission_form'
        self.fields['first_name'].css_class = 'form-control'
        terms_url =''
        if 'termscondsurl' in self.initial:
             terms_url = self.initial['termscondsurl']

        # START Get Annual Booking Periods
        if models.AdmissionsLocation.objects.filter(key=self.initial['loc']).count() > 0:
             al = models.AdmissionsLocation.objects.filter(key=self.initial['loc'])[0]
             apg = models.AnnualBookingPeriodGroup.objects.filter(mooring_group__in=[al.mooring_group.id,], status=1)
             booking_period_list = []
             booking_period_list.append(['','Please select a period'])
             for a in apg:
                   booking_period_list.append([a.id, a.name])
             self.fields['booking_period'].choices = booking_period_list

        discount_reason = []
        discount_reason.append(['','Please select a reason'])
        for d in self.initial['discount_reason']:
              discount_reason.append([d.id,d.text])
        self.fields['override_reason'].choices = discount_reason 
        vessel_tooltip = '<div align="left" class="tooltip2"><span class="tooltiptext" style="top: -60px;">Length must have two decimal places i.e. 9.00 metres or 12.35 metres</span><img height="14px" style="margin-bottom: 2px;" src="/static/img/information_icon.png"></div>'
        self.fields['vessel_length'].label = "Registered Vessel Length (meters) "+vessel_tooltip
        dynamic_selections = HTML('{% include "mooring/booking/annual_admission_form_js.html" %}')

        override_box = Div()
        if self.initial['allow_override_fees'] is True:
            override_box = Div('override_price_selection',HTML('<div class="small-12 medium-12 large-12 columns" style="display:none;" id="override_box">'),Fieldset('','override_price','override_reason','override_details'),HTML('</div>'))
        self.fields['terms'].label = "I agree to the <A href='"+terms_url+"' target='rottnest_admission_terms'>terms and conditions</A> (Including insurance requirements)"
        #override_box =HTML('<div class="small-12 medium-12 large-12 columns">')

        self.helper.layout = Layout(HTML("<div class='row'><div class='col-lg-6'>"),HTML('<div class="well"><h3 class="text-primary" style="text-align: center;">Personal Details</h3>'),'first_name','last_name','postal_address_line_1','postal_address_line_2',HTML("<div class='row'><div class='col-lg-6'>"),'country',HTML("</div><div class='col-lg-6'>"),'suburb',HTML('</div></div>'),HTML("<div class='row'><div class='col-lg-6'>"),'postcode',HTML("</div><div class='col-lg-6'>"),'state',HTML('</div></div>'),'mobile','phone','email','confirm_email',HTML('</div></div>'),HTML('<div class="col-lg-6">'),HTML('<div class="well"><h3 class="text-primary" style="text-align: center;">Vessel Details</h3>'),'vessel_rego','vessel_name','vessel_length',HTML('<h3 class="text-primary" style="text-align: center;">Annual Admission Period</h3>'),'booking_period', HTML('</div></div><div class="col-lg-12"><div class="well">'),HTML('<div class="row"><div class="col-md-12"><div class="row"><div class="col-md-6"><div class="form-group"><label for="Total Price">Total Price <span class="text-muted">(GST inclusive.)</span></label> <div class="input-group"><span class="input-group-addon">AUD $</span> <input type="text" id="id_total_price" readonly="readonly" class="form-control"></div></div></div></div>'),HTML('<div class="row"><div class="col-md-6"><div class="small-12 medium-12 large-4 columns"><label class="label-plain" style="width: 250px;">Click <a href="http://ria.wa.gov.au/about-us/Fees-and-charges" taget="_blank">here</a> for price information.</label>'),override_box,HTML('</div></div> <div class="col-md-6"><div class="row"><div class="col-md-12 "><div class="checkbox"><label>'),'terms',HTML('</div></div><div class="col-md-12 " style="margin-top: 20px; text-align: right;">'),Submit('ProceedtoPayment', 'Proceed to Payment', css_class='btn btn-primary'),HTML('</div></div></div></div>'),HTML('</div></div></div></div></div>'), dynamic_selections)


class FailedRefundCompletedForm(forms.ModelForm):

    class Meta:
        model = models.RefundFailed
        fields = []

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(FailedRefundCompletedForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.helper.form_id = 'id_refund_failed_form'
        #self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('Complete', 'Complete', css_class='btn-lg'))
        self.helper.add_input(Submit('cancel', 'Cancel', css_class='btn-lg'))

class BookingPeriodForm(forms.ModelForm):
    #mooring_group = ChoiceField(choices=[],)
    class Meta:
        model = models.BookingPeriod
        fields = ['name','mooring_group']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(BookingPeriodForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['mooring_group'].choices = []
        if 'mooring_group_choices'  in self.initial:
            self.fields['mooring_group'].choices = self.initial['mooring_group_choices']
        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})

        self.helper.form_id = 'id_change_group_form'
        if self.initial['action'] == 'edit':
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;'))

class AnnualBookingPeriodForm(forms.ModelForm):
    #mooring_group = ChoiceField(choices=[],)
    class Meta:
        model = models.AnnualBookingPeriodGroup
        fields = ['name','start_time','finish_time','status','mooring_group','letter']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(AnnualBookingPeriodForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['mooring_group'].choices = []
        if 'mooring_group_choices'  in self.initial:
            self.fields['mooring_group'].choices = self.initial['mooring_group_choices']
        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})
        vessel_category_pricing = HTML('{% include "mooring/dash/add_edit_annual_vessel_category.html" %}')

        print ("LETTER")
        print (self.initial['action'])
        if self.initial['action'] == 'new':
            del self.fields['letter']
        #self.initial['letter'].url = '/private-media/'
        #print (self.initial['letter'].url)
        self.helper.form_id = 'id_change_group_form'
        if self.initial['action'] == 'edit':
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;'))
        self.helper.layout = Layout('','')

class UpdateChangeGroupForm(forms.ModelForm):
    #mooring_group = ChoiceField(choices=[],)
    class Meta:
        model = models.ChangeGroup
        fields = ['name','mooring_group']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(UpdateChangeGroupForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['mooring_group'].choices = []
        if 'mooring_group_choices'  in self.initial:
            self.fields['mooring_group'].choices = self.initial['mooring_group_choices']
        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})

        self.helper.form_id = 'id_change_group_form'
        if self.initial['action'] == 'edit':
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;' ))


class UpdateCancelGroupForm(forms.ModelForm):

    class Meta:
        model = models.CancelGroup
        fields = ['name','mooring_group']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(UpdateCancelGroupForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['mooring_group'].choices = self.initial['mooring_group_choices']
#        self.fields['name'].class = 'form-control'
        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})

        self.helper.form_id = 'id_change_group_form'
        if self.initial['action'] == 'edit':
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;'))


class UpdateChangeOptionForm(forms.ModelForm):

    class Meta:
        model = models.ChangePricePeriod
        fields = ['calulation_type','percentage','amount','days']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(UpdateChangeOptionForm, self).__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
#        self.fields['name'].class = 'form-control'
        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})

        self.fields['percentage'].required = False
        self.fields['amount'].required = False
        self.helper.form_id = 'id_change_group_form'
        if self.initial['action'] == 'edit':
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;' ))


class UpdateCancelOptionForm(forms.ModelForm):

    class Meta:
        model = models.CancelPricePeriod
        fields = ['calulation_type','percentage','amount','days']

    def __init__(self, *args, **kwargs):
        # User must be passed in as a kwarg.
        super(UpdateCancelOptionForm, self).__init__(*args, **kwargs)

        self.helper = BaseFormHelper()
#        self.fields['name'].class = 'form-control'
        for f in self.fields:
           self.fields[f].widget.attrs.update({'class': 'form-control'})

        self.fields['percentage'].required = False
        self.fields['amount'].required = False

        self.helper.form_id = 'id_cancel_group_form'
        if self.initial['action'] == 'edit': 
           self.helper.add_input(Submit('Update', 'Update', css_class='btn-lg', style='margin-top: 15px;' ))
        else:
           self.helper.add_input(Submit('Create', 'Create', css_class='btn-lg', style='margin-top: 15px;' ))
   


class VehicleInfoForm(forms.Form):
    vehicle_rego = forms.CharField(label="Vessel Registration", widget=forms.TextInput(attrs={'required':True}))
    vehicle_type = forms.ChoiceField(label="Vessel Type", choices=VEHICLE_TYPES)
    entry_fee = forms.BooleanField(required=False, label="Entry fee")

VehicleInfoFormset = forms.formset_factory(VehicleInfoForm, extra=1, max_num=8)




class MakeBookingsForm(forms.Form):
    num_adult = forms.IntegerField(min_value=0, max_value=16, label="Adults (non-concessions)")
    num_child = forms.IntegerField(min_value=0, max_value=16, label="Children (ages 6-15)")
    num_concession = forms.IntegerField(min_value=0, max_value=16, label="Concessions")
    num_infant = forms.IntegerField(min_value=0, max_value=16, label="Infants (ages 0-5)")
    first_name = forms.CharField(label="Given Name(s)")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'required':True}), label="Last Name")
    phone = forms.CharField(widget=forms.TextInput(attrs={'required':True}), label="Phone (mobile preferred)")
    postcode = forms.CharField(max_length=4, label="Post Code",widget=forms.TextInput(attrs={'required':True}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), to_field_name="iso_3166_1_a2")
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'required':True}))
    confirm_email = forms.EmailField(label ="Confirm Email", widget=forms.TextInput(attrs={'required':True}))

    def __init__(self, *args, **kwargs):
        super(MakeBookingsForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['required'] = True 

    def clean(self):
        super(MakeBookingsForm, self).clean()

#        if ('num_adult' in self.cleaned_data and 'num_concession' in self.cleaned_data):
        if ('num_mooring' in self.cleaned_data):
            if (self.cleaned_data.get('num_mooring')) < 1:
                raise forms.ValidationError('Booking requires at least 1 guest that is an adult or concession.')



class AnonymousMakeBookingsForm(MakeBookingsForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'required':True}))
    confirm_email = forms.EmailField(label ="Confirm Email", widget=forms.TextInput(attrs={'required':True}))

    def clean(self):
        super(AnonymousMakeBookingsForm, self).clean()

        if ('email' in self.cleaned_data and 'confirm_email' in self.cleaned_data):
            if (self.cleaned_data.get('email') != self.cleaned_data.get('confirm_email')):
                raise forms.ValidationError('Email and confirmation email fields do not match.')

