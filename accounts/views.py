from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.audit import log_action
from accounts.decorators import role_required
from accounts.forms import EmailAuthenticationForm, UserRegistrationForm, UserStatusForm
from accounts.models import AuditLog, Role, User

class EmailLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm

    def get_success_url(self):
        return self.get_redirect_url() or '/'

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@role_required(Role.ADMIN)
def user_list(request):
    users = User.objects.select_related('person', 'role').order_by('person__surname')
    return render(request, 'accounts/user_list.html', {'users': users})

@role_required(Role.ADMIN)
def user_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account created.')
            return redirect('accounts:user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/user_form.html', {'form': form})

@role_required(Role.ADMIN)
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserStatusForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account updated.')
            return redirect('accounts:user_list')
    else:
        form = UserStatusForm(instance=user)
    return render(request, 'accounts/user_status_form.html', {'form': form, 'user_obj': user})

@role_required(Role.ADMIN)
def audit_log_list(request):
    logs = AuditLog.objects.select_related('user').all()[:200]
    return render(request, 'accounts/audit_log_list.html', {'logs': logs})

@role_required(Role.ADMIN)
@require_POST
def trigger_backup(request):
    log_action('BACKUP', 'System')
    return JsonResponse({'status': 'ok'})
