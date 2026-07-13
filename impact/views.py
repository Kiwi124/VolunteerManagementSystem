from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from accounts.decorators import role_required
from accounts.models import Role
from impact.forms import ReportForm
from impact.models import Report
from impact.services import (
    COST_RANGE_CHOICES,
    organisation_metrics,
    programme_metrics,
    resolve_cost_window,
    total_programme_cost,
)

IMPACT_MANAGERS = (
    Role.ADMIN,
    Role.FUNDER_RELATIONS_MANAGER,
)

DASHBOARD_VIEWERS = IMPACT_MANAGERS + (Role.OPERATIONS_MANAGER, Role.PROGRAMME_COORDINATOR)

@role_required(*DASHBOARD_VIEWERS)
def impact_dashboard(request):
    selected_range = request.GET.get('range', 'all')
    custom_start = parse_date(request.GET.get('start') or '')
    custom_end = parse_date(request.GET.get('end') or '')
    window_start, window_end = resolve_cost_window(selected_range, custom_start, custom_end)
    context = {
        'metrics': organisation_metrics(),
        'total_cost': total_programme_cost(window_start, window_end),
        'cost_range_choices': COST_RANGE_CHOICES,
        'selected_range': selected_range,
        'custom_start': custom_start,
        'custom_end': custom_end,
    }
    return render(request, 'impact/dashboard.html', context)

@role_required(*IMPACT_MANAGERS)
def report_list(request):
    reports = Report.objects.select_related('programme').order_by('-report_date')
    return render(request, 'impact/report_list.html', {'reports': reports})

@role_required(*IMPACT_MANAGERS)
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save()
            return redirect('impact:report_detail', report_id=report.report_id)
    else:
        form = ReportForm()
    return render(request, 'impact/report_form.html', {'form': form})

@role_required(*IMPACT_MANAGERS)
def report_detail(request, report_id):
    report = get_object_or_404(Report.objects.select_related('programme'), pk=report_id)
    return render(request, 'impact/report_detail.html', {
        'report': report,
        'metrics': programme_metrics(report.programme),
    })
