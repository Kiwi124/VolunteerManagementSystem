from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import Role
from programmes.forms import EventForm, ProgrammeForm, VolunteerAssignmentForm
from programmes.models import Event, Programme, VolunteerAssignment

PROGRAMME_MANAGERS = (
    Role.ADMIN,
    Role.OPERATIONS_MANAGER,
    Role.PROGRAMME_COORDINATOR,
)


@role_required(*PROGRAMME_MANAGERS)
def programme_list(request):
    programmes = Programme.objects.select_related('status').order_by('-start_date')
    return render(request, 'programmes/programme_list.html', {'programmes': programmes})


@role_required(*PROGRAMME_MANAGERS)
def programme_create(request):
    if request.method == 'POST':
        form = ProgrammeForm(request.POST)
        if form.is_valid():
            programme = form.save()
            messages.success(request, 'Programme created.')
            return redirect('programmes:programme_detail', programme_id=programme.programme_id)
    else:
        form = ProgrammeForm()
    return render(request, 'programmes/programme_form.html', {'form': form})


@role_required(*PROGRAMME_MANAGERS)
def programme_edit(request, programme_id):
    programme = get_object_or_404(Programme, pk=programme_id)
    if request.method == 'POST':
        form = ProgrammeForm(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            messages.success(request, 'Programme updated.')
            return redirect('programmes:programme_detail', programme_id=programme.programme_id)
    else:
        form = ProgrammeForm(instance=programme)
    return render(request, 'programmes/programme_form.html', {'form': form, 'programme': programme})


@role_required(*PROGRAMME_MANAGERS)
def programme_detail(request, programme_id):
    programme = get_object_or_404(Programme, pk=programme_id)
    events = programme.events.select_related('status').order_by('start_date')
    return render(request, 'programmes/programme_detail.html', {'programme': programme, 'events': events})


@role_required(*PROGRAMME_MANAGERS)
def event_create(request, programme_id):
    programme = get_object_or_404(Programme, pk=programme_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.programme = programme
            event.save()
            form.save_m2m()
            messages.success(request, 'Event created.')
            return redirect('programmes:event_detail', event_id=event.event_id)
    else:
        form = EventForm()
    return render(request, 'programmes/event_form.html', {'form': form, 'programme': programme})


@role_required(*PROGRAMME_MANAGERS)
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated.')
            return redirect('programmes:event_detail', event_id=event.event_id)
    else:
        form = EventForm(instance=event)
    return render(request, 'programmes/event_form.html', {'form': form, 'programme': event.programme})


@role_required(*PROGRAMME_MANAGERS)
def event_detail(request, event_id):
    event = get_object_or_404(Event.objects.select_related('programme', 'status'), pk=event_id)
    assignments = event.assignments.select_related('user__person')
    return render(request, 'programmes/event_detail.html', {
        'event': event,
        'assignments': assignments,
        'assignment_form': VolunteerAssignmentForm(),
    })


@role_required(*PROGRAMME_MANAGERS)
def assignment_add(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = VolunteerAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.event = event
            assignment.save()
            messages.success(request, 'Volunteer assigned.')
    return redirect('programmes:event_detail', event_id=event_id)


@role_required(*PROGRAMME_MANAGERS)
def assignment_attendance_toggle(request, assignment_id):
    assignment = get_object_or_404(VolunteerAssignment, pk=assignment_id)
    if request.method == 'POST':
        assignment.attendance = not assignment.attendance
        assignment.save(update_fields=['attendance'])
    return redirect('programmes:event_detail', event_id=assignment.event_id)


@role_required(*PROGRAMME_MANAGERS)
def assignment_remove(request, assignment_id):
    assignment = get_object_or_404(VolunteerAssignment, pk=assignment_id)
    event_id = assignment.event_id
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment removed.')
    return redirect('programmes:event_detail', event_id=event_id)
