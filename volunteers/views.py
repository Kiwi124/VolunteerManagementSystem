from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import Role, User
from programmes.models import Event, VolunteerAssignment
from volunteers.forms import (
    AvailabilityForm,
    DBSStatusForm,
    PersonForm,
    SkillForm,
    VolunteerRegistrationForm,
    VolunteerSkillForm,
)
from volunteers.models import Availability, Skill, VolunteerSkill

VOLUNTEER_MANAGERS = (
    Role.ADMIN,
    Role.PROGRAMME_COORDINATOR,
    Role.VOLUNTEER_COORDINATOR,
    Role.OPERATIONS_MANAGER,
)

def _volunteer_queryset():
    return User.objects.filter(role__role_name=Role.VOLUNTEER).select_related('person', 'role')

@role_required(*VOLUNTEER_MANAGERS)
def volunteer_list(request):
    volunteers = _volunteer_queryset().order_by('person__surname')
    return render(request, 'volunteers/volunteer_list.html', {'volunteers': volunteers})

@role_required(*VOLUNTEER_MANAGERS)
def volunteer_register(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            messages.success(request, 'Volunteer registered.')
            return redirect('volunteers:volunteer_detail', user_id=volunteer.user_id)
    else:
        form = VolunteerRegistrationForm()
    return render(request, 'volunteers/volunteer_register.html', {'form': form})

@role_required(*VOLUNTEER_MANAGERS)
def volunteer_detail(request, user_id):
    volunteer = get_object_or_404(_volunteer_queryset(), pk=user_id)
    dbs_statuses = volunteer.person.dbs_statuses.order_by('-dbs_status_id')
    availabilities = volunteer.availabilities.order_by('day_of_week', 'start_time')
    skills = volunteer.volunteer_skills.select_related('skill')
    context = {
        'volunteer': volunteer,
        'dbs_statuses': dbs_statuses,
        'availabilities': availabilities,
        'skills': skills,
        'availability_form': AvailabilityForm(),
        'skill_form': VolunteerSkillForm(),
        'dbs_form': DBSStatusForm(),
    }
    return render(request, 'volunteers/volunteer_detail.html', context)

@role_required(*VOLUNTEER_MANAGERS)
def person_edit(request, user_id):
    volunteer = get_object_or_404(_volunteer_queryset(), pk=user_id)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=volunteer.person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer details updated.')
            return redirect('volunteers:volunteer_detail', user_id=user_id)
    else:
        form = PersonForm(instance=volunteer.person)
    return render(request, 'volunteers/person_form.html', {'form': form, 'volunteer': volunteer})

@role_required(*VOLUNTEER_MANAGERS)
def dbs_status_add(request, user_id):
    volunteer = get_object_or_404(_volunteer_queryset(), pk=user_id)
    if request.method == 'POST':
        form = DBSStatusForm(request.POST)
        if form.is_valid():
            dbs = form.save(commit=False)
            dbs.person = volunteer.person
            dbs.save()
            messages.success(request, 'DBS status recorded.')
    return redirect('volunteers:volunteer_detail', user_id=user_id)

@role_required(*VOLUNTEER_MANAGERS)
def availability_add(request, user_id):
    volunteer = get_object_or_404(_volunteer_queryset(), pk=user_id)
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = volunteer
            availability.save()
            messages.success(request, 'Availability added.')
    return redirect('volunteers:volunteer_detail', user_id=user_id)

@role_required(*VOLUNTEER_MANAGERS)
def availability_delete(request, availability_id):
    availability = get_object_or_404(Availability, pk=availability_id)
    user_id = availability.user_id
    if request.method == 'POST':
        availability.delete()
        messages.success(request, 'Availability removed.')
    return redirect('volunteers:volunteer_detail', user_id=user_id)

@role_required(*VOLUNTEER_MANAGERS)
def volunteer_skill_add(request, user_id):
    volunteer = get_object_or_404(_volunteer_queryset(), pk=user_id)
    if request.method == 'POST':
        form = VolunteerSkillForm(request.POST)
        if form.is_valid():
            volunteer_skill = form.save(commit=False)
            volunteer_skill.user = volunteer
            volunteer_skill.save()
            messages.success(request, 'Skill added.')
    return redirect('volunteers:volunteer_detail', user_id=user_id)

@role_required(*VOLUNTEER_MANAGERS)
def volunteer_skill_delete(request, volunteer_skill_id):
    volunteer_skill = get_object_or_404(VolunteerSkill, pk=volunteer_skill_id)
    user_id = volunteer_skill.user_id
    if request.method == 'POST':
        volunteer_skill.delete()
        messages.success(request, 'Skill removed.')
    return redirect('volunteers:volunteer_detail', user_id=user_id)

@role_required(*VOLUNTEER_MANAGERS)
def skill_list(request):
    skills = Skill.objects.order_by('skill_name')
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill added to catalogue.')
            return redirect('volunteers:skill_list')
    else:
        form = SkillForm()
    return render(request, 'volunteers/skill_list.html', {'skills': skills, 'form': form})


@login_required
def my_events(request):
    """View for volunteers to see their upcoming and past events."""
    now = timezone.now()
    
    # Get all assignments for the current user
    assignments = request.user.assignments.select_related(
        'event__programme', 'event__status'
    ).order_by('event__start_date')
    
    # Separate upcoming and past events
    upcoming_assignments = [
        a for a in assignments if a.event.start_date > now
    ]
    past_assignments = [
        a for a in assignments if a.event.end_date <= now
    ]
    
    # Sort past events by most recent first
    past_assignments.sort(key=lambda x: x.event.end_date, reverse=True)
    
    context = {
        'upcoming_assignments': upcoming_assignments,
        'past_assignments': past_assignments,
    }
    return render(request, 'volunteers/my_events.html', context)

