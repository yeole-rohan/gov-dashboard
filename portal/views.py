from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .models import User, Taluka, Panchayat, Agency, Confirmation, Payment, Grampanchayat, Audit
from .forms import GPSignUPForm, CEOSignUpForm, S2SignUpForm, ObservarSignUpForm, PublicForm, GovermentForm, CertifiedForm, ConfirmationForm, PaymentForm, PaymentApproveForm, UTRapproveForm, AuditForm, AuditSelectForm, AuditEditForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from goverment import settings


# Create your views here.

'''Deafult Home View'''
@login_required
def home(request):
    confirmtwo, paytwo, confirmthree, paythree, auditthree, auditfour, confirmfour,payfour, payone = '', '','','','', '','','',''
    try:
        get_gov_selected_agency = Agency.objects.filter (user = request.user.id, choose_goverment='True')
        confirmone = Confirmation.objects.filter(user=request.user.id, phaseno__iexact=1)
        payone = Payment.objects.get(user=request.user.id, phaseno=1)
        confirmtwo = Confirmation.objects.filter(user=request.user.id, phaseno__iexact=2)
        paytwo = Payment.objects.get(user=request.user.id, phaseno=2)
        confirmthree = Confirmation.objects.filter(user=request.user.id, phaseno__iexact=3)
        paythree = Payment.objects.get(user=request.user.id, phaseno=3)
        auditthree = Audit.objects.get(user=request.user.id, phaseno=3)
        auditfour = Audit.objects.get(user=request.user.id, phaseno=4)
        confirmfour = Confirmation.objects.filter(user=request.user.id, phaseno__iexact=4)
        payfour = Payment.objects.get(user=request.user.id, phaseno=4)
    except:
        pass 
    if request.user.is_gp:
        if get_gov_selected_agency:
            if confirmone:
                if payone:
                    if payone.status == "unmatched":
                        return redirect("portal:utr_missed")
                    elif payone.status == "matched":
                        if confirmtwo:
                            if paytwo:
                                if paytwo.status == "unmatched":
                                    return redirect("portal:utr_missedtwo")
                                elif paytwo.status == "matched":
                                    if confirmthree:
                                        if paythree:
                                            if paythree.status =="unmatched":
                                                return redirect("portal:utr_missedthree")
                                            elif paythree.status =="matched":
                                                if auditthree.status =="unmatched":
                                                    return redirect("portal:audit_miss")
                                                elif auditthree.status =="matched":
                                                    if confirmfour:
                                                        if payfour:
                                                            if payfour.status =="unmatched":
                                                                return redirect("portal:utr_missedfour")
                                                            elif payfour.status =="matched":
                                                                if auditfour.status =="unmatched":
                                                                    return redirect("portal:audit_miss_four")
                                                                elif auditfour.status =="matched":
                                                                    return redirect("portal:index")
                                                                return redirect("portal:audit_msg")
                                                            return redirect("portal:pending4")
                                                        return redirect("portal:pay4")
                                                    return redirect("portal:index")
                                                return redirect("portal:audit_msg")
                                            return redirect("portal:pending3")
                                        return redirect("portal:pay3")
                                    return redirect("portal:index")
                                return redirect("portal:pending2")
                            return redirect("portal:pay2")
                        return redirect("portal:index")
                    return redirect('portal:pending1')
                return redirect('portal:pay1')
            return redirect('portal:confirm1')
    get_local_selected_agency = ''
    try:
        get_local_selected_agency = Agency.objects.filter (user = request.user.id, choose_local='True')
    except:
        pass
    if request.user.is_gp:
        if get_local_selected_agency:
            return redirect("portal:local")
    
    get_certified_selected_agency = ''
    try:
        get_certified_selected_agency = Agency.objects.filter (user = request.user.id, choose_local='True')
    except:
        pass
    if request.user.is_gp:
        if get_certified_selected_agency:
            return redirect("portal:local")
    gov_choose = GovermentForm()
    pub_form = PublicForm()
    certified = CertifiedForm()
    if request.method == "POST" and "goverment" in request.POST:
        gov_choose = GovermentForm(request.POST or None)
        if gov_choose.is_valid():
            gov_choose = gov_choose.save(commit=False)
            gov_choose.user = request.user
            gov_choose.save()
            return redirect('portal:confirm1')

    if request.method == "POST" and "public" in request.POST:
        pub_form = PublicForm(request.POST or None)
        if pub_form.is_valid():
            pub_form = pub_form.save(commit=False)
            pub_form.user = request.user
            pub_form.save()
            return redirect('portal:local')

    if request.method == "POST" and "certified" in request.POST:
        certified = CertifiedForm(request.POST or None)
        if certified.is_valid():
            certified = certified.save(commit=False)
            certified.user = request.user
            certified.already_certified = "True"
            certified.save()
            return redirect('portal:local')

    return render(request, template_name="dashboard.html", context={'pub_form' : pub_form, 'gov_choose' : gov_choose, 'certified' : certified})

''' S2 dashboard '''
def s2dashboard(request):
    all_pending_payments = Payment.objects.filter(utrno__isnull=False, status__iexact='Pending')
    all_matched_payments = Payment.objects.filter(utrno__isnull=False, status__iexact='Matched')
    all_unmatched_payments = Payment.objects.filter(utrno__isnull=False, status__iexact='Unmatched')
    all_pending_audits = Audit.objects.filter(status__iexact='Pending')
    all_matched_audits = Audit.objects.filter(status__iexact='Matched')
    

    return render(request, template_name="s2/s2-dashboard.html", context={'all_pending_payments': all_pending_payments, 'all_matched_payments' : all_matched_payments, 'all_unmatched_payments' : all_unmatched_payments, 'all_pending_audits' : all_pending_audits, 'all_matched_audits' : all_matched_audits})

'''observar'''
def observar(request):
    all_matched_payments = Payment.objects.filter(utrno__isnull=False, status__iexact='Matched')
    all_users = Grampanchayat.objects.all().count()
    get_count_confirm = Payment.objects.filter(phaseno=1).count()
    get_count_confirm = Payment.objects.filter(phaseno=1).count()
    get_count_confirm_pending = Confirmation.objects.filter(phaseno=1).count()
    get_count_local = Agency.objects.filter(choose_local=True).count()
    return render(request, template_name="ob-dashboard.html", context={'all_matched_payments' : all_matched_payments, 'get_count_confirm' : get_count_confirm, 'get_count_confirm_pending' : get_count_confirm_pending, 'all_users' : all_users,'get_count_local': get_count_local})

''' Index Page '''
def index(request):

    phaseonepay = Payment.objects.filter(user=request.user.id, phaseno=1)
    phasetwopay = Payment.objects.filter(user=request.user.id, phaseno=2)
    phasethreepay = Payment.objects.filter(user=request.user.id, phaseno=3)
    phasefourpay = Payment.objects.filter(user=request.user.id, phaseno=4)
        
    return render(request, template_name="index.html", context={'phaseonepay' : phaseonepay, 'phasetwopay' : phasetwopay, 'phasethreepay' : phasethreepay, 'phasefourpay' : phasefourpay})

def local(request):
    return render(request, template_name="local/local.html", context={})
def audit_edit_four(request, id):
    audit = AuditEditForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        audit = AuditEditForm(request.POST or None, request.FILES)
        if audit.is_valid():
            files = audit.cleaned_data['files']
            content_type  = files.content_type.split('/')[1]
            if content_type in settings.CONTENT_TYPES_IMG:
                if files.size > int(settings.MAX_UPLOAD_SIZE_IMG):
                    messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE_IMG), filesizeformat(files.size)))
                else:
                    Audit.objects.filter(id=id).update(document=files)
                    return redirect('portal:pending4')
            else:
                messages.error(request, "File is not supported")
    return render(request, template_name="audit/audit-miss-update.html", context={'audit_form' : audit}) 

''' Stage four confirm '''
def confirm4(request):
    try:
        audit_obj = Audit.objects.filter(user=request.user.id, phaseno=4)
    except:
        pass
    confirm = ConfirmationForm()
    audit = AuditForm()
    if request.method == "POST" and "audit" in request.POST:
        current_user = get_object_or_404(User, id=request.user.id)
        audit = AuditForm(request.POST or None, request.FILES)
        print(audit.is_valid())
        if audit.is_valid():
            print(audit.is_valid())
            files = audit.cleaned_data['document']
            content_type  = files.content_type.split('/')[1]
            print(files)
            print(files.size)
            print(files.content_type)
            print(files.content_type.split())
            if content_type in settings.CONTENT_TYPES_IMG:
                if files.size > int(settings.MAX_UPLOAD_SIZE_IMG):
                    messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE_IMG), filesizeformat(files.size)))
                else:
                    audit = audit.save(commit=False)
                    audit.phaseno = 4
                    audit.save()
                    audit.user.add(current_user.id)
                    audit.save()
                    return redirect('portal:confirm4')
            else:
                messages.error(request, "File is not supported")

    if request.method == "POST" and "confirm" in request.POST:
        current_user = get_object_or_404(User, id=request.user.id)
        confirm = ConfirmationForm(request.POST or None)
        if confirm.is_valid():
            confirm = confirm.save(commit=False)
            confirm.phaseno = 4
            confirm.save()
            confirm.user.add(current_user.id)
            confirm.save()
            return redirect('portal:pay4')
    return render(request, template_name="confirmation/confirm4.html", context={'confirm' : confirm, 'audit' : audit, 'audit_obj' : audit_obj}) 
''' Stage Three Audit Approve'''
def audit_approve(request, id):
    get_audit = Audit.objects.get(id=id, status='pending')
    audit_form = AuditSelectForm()
    if request.method == "POST":
        audit_form = AuditSelectForm(request.POST or None)
        if audit_form.is_valid():
            select_check = audit_form.cleaned_data['select_check']
            Audit.objects.filter(id=id).update(status=select_check) 
            return redirect('portal:s2dashboard')
    return render (request, template_name="audit/audit-confirm.html", context={'audit_form' : audit_form})

''' Stage Three Confirmation '''
def confirm3(request):
    try:
        audit_obj = Audit.objects.filter(user=request.user.id, phaseno=3)
    except:
        pass
    confirm = ConfirmationForm()
    audit = AuditForm()
    if request.method == "POST" and "audit" in request.POST:
        current_user = get_object_or_404(User, id=request.user.id)
        audit = AuditForm(request.POST or None, request.FILES)
        print(audit.is_valid())
        if audit.is_valid():
            print(audit.is_valid())
            files = audit.cleaned_data['document']
            content_type  = files.content_type.split('/')[1]
            print(files)
            print(files.size)
            print(files.content_type)
            print(files.content_type.split())
            if content_type in settings.CONTENT_TYPES:
                if files.size > int(settings.MAX_UPLOAD_SIZE):
                    messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(files.size)))
                else:
                    audit = audit.save(commit=False)
                    audit.phaseno = 3
                    audit.save()
                    audit.user.add(current_user.id)
                    audit.save()
                    return redirect('portal:confirm3')
            else:
                messages.error(request, "File is not supported")

    if request.method == "POST" and "confirm" in request.POST:
        current_user = get_object_or_404(User, id=request.user.id)
        confirm = ConfirmationForm(request.POST or None)
        if confirm.is_valid():
            confirm = confirm.save(commit=False)
            confirm.phaseno = 3
            confirm.save()
            confirm.user.add(current_user.id)
            confirm.save()
            return redirect('portal:pay3')
    return render(request, template_name="confirmation/confirm3.html", context={'confirm' : confirm, 'audit' : audit, 'audit_obj' : audit_obj}) 

''' Stage Three pending Audit '''
def audit_msg(request):
    return render (request, template_name="audit/audit-info-msg.html", context={})
''' Stage Three pending Confirmation '''
def pending3(request):
    return render (request, template_name="pay-pending/pending3.html", context={})
''' Stage Four pending Confirmation '''
def pending4(request):
    return render (request, template_name="pay-pending/pending4.html", context={})
def payment4(request):
    pay4 = PaymentForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        pay4 = PaymentForm(request.POST or None)
        if pay4.is_valid():
            pay4 = pay4.save(commit=False)
            pay4.phaseno = 4
            pay4.save()
            pay4.user.add(current_user.id)
            pay4.save()
            return redirect('portal:pending4')
    return render(request, template_name="payments/pay4.html", context={'pay4' : pay4})

def payment3(request):
    pay3 = PaymentForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        pay3 = PaymentForm(request.POST or None)
        if pay3.is_valid():
            pay3 = pay3.save(commit=False)
            pay3.phaseno = 3
            pay3.save()
            pay3.user.add(current_user.id)
            pay3.save()
            return redirect('portal:pending3')
    return render(request, template_name="payments/pay3.html", context={'pay3' : pay3})

def audit_edit(request, id):
    audit = AuditEditForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        audit = AuditEditForm(request.POST or None, request.FILES)
        print(audit.is_valid())
        if audit.is_valid():
            print(audit.is_valid())
            files = audit.cleaned_data['files']
            content_type  = files.content_type.split('/')[1]
            print(files)
            print(files.size)
            print(files.content_type)
            print(files.content_type.split())
            if content_type in settings.CONTENT_TYPES:
                if files.size > int(settings.MAX_UPLOAD_SIZE):
                    messages.error(request, "Please keep filesize under {}. Current filesize {}".format(filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(files.size)))
                else:
                    Audit.objects.filter(id=id).update(document=files)
                    return redirect('portal:pending3')
            else:
                messages.error(request, "File is not supported")
    return render (request, template_name="audit/audit-edit.html", context={'audit_form' : audit})


''' Stage Four Audit Missed '''
def audit_miss_four(request):
    get_audit = Audit.objects.get(user=request.user.id, status='unmatched')
    return render (request, template_name="audit/audit-not-matched-four.html", context={'get_audit' : get_audit})


''' Stage Three Audit Missed '''
def audit_miss(request):
    get_audit = Audit.objects.get(user=request.user.id, status='unmatched')
    return render (request, template_name="audit/audit-not-matched.html", context={'get_audit' : get_audit})

''' Stage Two Confirmation '''
def confirm2(request):
    confirm = ConfirmationForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        confirm = ConfirmationForm(request.POST or None)
        if confirm.is_valid():
            confirm = confirm.save(commit=False)
            confirm.phaseno = 2
            confirm.save()
            confirm.user.add(current_user.id)
            confirm.save()
            return redirect('portal:pay2')
    return render(request, template_name="confirmation/confirm2.html", context={'confirm' : confirm}) 

''' Stage two Payment'''
def payment2(request):
    pay2 = PaymentForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        pay2 = PaymentForm(request.POST or None)
        if pay2.is_valid():
            pay2 = pay2.save(commit=False)
            pay2.phaseno = 2
            pay2.save()
            pay2.user.add(current_user.id)
            pay2.save()
            return redirect('portal:pending2')
    return render(request, template_name="payments/pay2.html", context={'pay2' : pay2})

''' Stage two pending Confirmation '''
def pending2(request):
    return render (request, template_name="pay-pending/pending2.html", context={})

''' UTR change '''
def utr_change(request, id):
    paymiss = ''
    url = ''
    try:
        paymiss = Payment.objects.get(user=request.user.id, phaseno=1, status="unmatched")
        url = "pending1"
    except:
        pass
    utrform = UTRapproveForm() 
    if request.method == "POST":
        utrform = UTRapproveForm(request.POST or None)
        if utrform.is_valid():
            utr_no = utrform.cleaned_data['utr']
            Payment.objects.filter(user=request.user.id, id=id).update(status="pending", utrno=utr_no)
            return redirect('portal:pending1')
    return render(request, template_name="UTR/utr-change.html", context={'utrform' : utrform, 'paymiss' : paymiss})

''' UTR change four'''
def utr_changefour(request, id):
    paymiss = ''
    try:
        paymiss = Payment.objects.get(user=request.user.id, phaseno=4, status="unmatched")
    except:
        pass
    utrform = UTRapproveForm() 
    if request.method == "POST":
        utrform = UTRapproveForm(request.POST or None)
        if utrform.is_valid():
            utr_no = utrform.cleaned_data['utr']
            Payment.objects.filter(user=request.user.id, id=id).update(status="pending", utrno=utr_no)
            return redirect('portal:pending4')
    return render(request, template_name="UTR/utr-changefour.html", context={'utrform' : utrform, 'paymiss' : paymiss})

''' UTR change three'''
def utr_changethree(request, id):
    paymiss = ''
    try:
        paymiss = Payment.objects.get(user=request.user.id, phaseno=3, status="unmatched")
    except:
        pass
    utrform = UTRapproveForm() 
    if request.method == "POST":
        utrform = UTRapproveForm(request.POST or None)
        if utrform.is_valid():
            utr_no = utrform.cleaned_data['utr']
            Payment.objects.filter(user=request.user.id, id=id).update(status="pending", utrno=utr_no)
            return redirect('portal:pending3')
    return render(request, template_name="UTR/utr-changethree.html", context={'utrform' : utrform, 'paymiss' : paymiss})

''' utr missed three '''
def utr_missedfour(request):
    paymiss = ''
    try:
        stage = "Four"
        paymiss = Payment.objects.get(user=request.user.id, phaseno=4, status="unmatched")
    except: 
        pass
    return render(request, template_name="UTR/utrfour.html", context={'paymiss' : paymiss, 'stage' : stage})

''' utr missed three '''
def utr_missedthree(request):
    paymiss = ''
    try:
        stage = "Three"
        paymiss = Payment.objects.get(user=request.user.id, phaseno=3, status="unmatched")
    except: 
        pass
    return render(request, template_name="UTR/utrthree.html", context={'paymiss' : paymiss, 'stage' : stage})

''' UTR change two'''
def utr_changetwo(request, id):
    paymiss = ''
    try:
        paymiss = Payment.objects.get(user=request.user.id, phaseno=2, status="unmatched")
        url = "pending2"
    except:
        pass
    utrform = UTRapproveForm() 
    if request.method == "POST":
        utrform = UTRapproveForm(request.POST or None)
        if utrform.is_valid():
            utr_no = utrform.cleaned_data['utr']
            Payment.objects.filter(user=request.user.id, id=id).update(status="pending", utrno=utr_no)
            return redirect('portal:pending2')
    return render(request, template_name="UTR/utr-changetwo.html", context={'utrform' : utrform, 'paymiss' : paymiss})

''' UTR Missmatched '''
def utr_missed(request):
    paymiss = ''
    try:
        stage = "One"
        paymiss = Payment.objects.get(user=request.user.id, phaseno=1, status="unmatched")
    except:
        pass
    return render(request, template_name="UTR/utr.html", context={'paymiss' : paymiss})

''' UTR Missmatched '''
def utr_missedtwo(request):
    paymiss = ''
    try:
        paymiss = Payment.objects.get(user=request.user.id, phaseno=2, status="unmatched")
    except:
        pass
    return render(request, template_name="UTR/utrtwo.html", context={'paymiss' : paymiss})

''' UTR Matched '''
def utr_matched(request):
    return render(request, template_name="UTR/pay-cofirm.html", context={})

''' S2 confirms payments '''
def confirm_payment(request, pay_id, user_id): 
    get_payment = Payment.objects.get(id=pay_id)
    pay_approve = PaymentApproveForm()
    if request.method == "POST":
        pay_approve = PaymentApproveForm(request.POST or None)
        get_gp_user = get_object_or_404(Grampanchayat, user_id=user_id)
        if pay_approve.is_valid():
            pay_choice = pay_approve.cleaned_data['pay']
            remark = pay_approve.cleaned_data['remark']
            Payment.objects.filter(user=get_gp_user, id=pay_id).update(status=pay_choice, remark=remark)
            return redirect('portal:s2dashboard' )
    return render(request, template_name="s2/s2-confirm.html", context={'get_payment' : get_payment, 'pay_approve' : pay_approve})

''' Stage One Confirmation '''
def confirm1(request):
    confirm = ConfirmationForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        confirm = ConfirmationForm(request.POST or None)
        if confirm.is_valid():
            confirm = confirm.save(commit=False)
            confirm.phaseno = 1
            confirm.save()
            confirm.user.add(current_user.id)
            confirm.save()
            return redirect('portal:pay1')
    return render(request, template_name="confirmation/confirm1.html", context={'confirm' : confirm})

''' Stage One Payment'''
def payment1(request):
    pay1 = PaymentForm()
    if request.method == "POST":
        current_user = get_object_or_404(User, id=request.user.id)
        pay1 = PaymentForm(request.POST or None)
        if pay1.is_valid():
            pay1 = pay1.save(commit=False)
            pay1.phaseno = 1
            pay1.save()
            pay1.user.add(current_user.id)
            pay1.save()
            return redirect('portal:pending1')
    return render(request, template_name="payments/pay1.html", context={'pay1' : pay1})

''' Stage One pending Confirmation '''
def pending1(request):
    return render (request, template_name="pay-pending/pending1.html", context={})

'''Ajax calling views for dropdown from grampanchayat register view'''
def load_taluka(request):
    district_id = request.GET.get('district')
    talukas = Taluka.objects.filter(district=district_id).order_by('taluka')
    return render(request, template_name="ajax/talukadropdown.html", context={ 'talukas' : talukas })

def load_panchayat(request): 
    taluka_id = request.GET.get('taluka')
    panchayat = Panchayat.objects.filter(taluka=taluka_id).order_by('panchayat')
    return render(request, template_name="ajax/panchayatdropdown.html", context={ 'panchayats' : panchayat })


'''Grampanchayat Register View'''
class GPRegister(CreateView):
    model = User
    form_class = GPSignUPForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

'''CEO Register View'''
class CEORegister(CreateView):
    model = User
    form_class = CEOSignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

'''S2 Register View'''
class S2Regsiter(CreateView):
    model = User
    form_class= S2SignUpForm
    template_name = 'registration/User-Sign-Up.html'
    success_url = reverse_lazy('login')

'''Observar Register View'''
class ObservarRegsiter(CreateView):
    model = User
    form_class= ObservarSignUpForm
    template_name = 'registration/User-Sign-Up.html'
    success_url = reverse_lazy('login')
