"""
Frontend Views for Credentials Manager
This module contains UI views that handle user interactions and presentation logic.
All business logic is delegated to the backend app.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

# Import models from backend
from apps.backend.models import Credentials, SecureNote, ActivityLog
from apps.backend.forms import CredentialForm, SecureNoteForm, SearchForm

# Import business logic from backend
from apps.backend.business_logic import (
    DashboardManager, CredentialsManager, SecureNotesManager,
    ActivityManager, SearchManager, PaginationManager,
    FavoriteManager, AccessTracker, DataExportManager
)


@login_required
def dashboard(request):
    """Main dashboard page"""
    # Get dashboard data using business logic
    dashboard_data = DashboardManager.get_dashboard_stats(request.user)
    
    context = {
        'total_credentials': dashboard_data['total_credentials'],
        'total_notes': dashboard_data['total_notes'],
        'favorite_credentials': dashboard_data['favorite_credentials'],
        'favorite_notes': dashboard_data['favorite_notes'],
        'recent_activities': dashboard_data['recent_activities'],
        'recent_credentials': dashboard_data['recent_credentials'],
        'recent_notes': dashboard_data['recent_notes'],
        'credential_types': dashboard_data['credential_types'],
    }
    
    return render(request, 'frontend/dashboard.html', context)


@login_required
def credentials_list(request):
    """List all credentials with search and filter"""
    form = SearchManager.get_search_form(request.GET)
    
    # Get search parameters
    search_params = {}
    if form.is_valid():
        search_params = {
            'query': form.cleaned_data.get('query'),
            'type_filter': form.cleaned_data.get('type_filter'),
            'favorites_only': form.cleaned_data.get('favorites_only'),
        }
    
    # Get credentials using business logic
    credentials = CredentialsManager.get_user_credentials(request.user, search_params)
    
    # Paginate results
    page_obj = PaginationManager.paginate_queryset(credentials, request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_count': credentials.count(),
    }
    
    return render(request, 'frontend/credentials_list.html', context)


@login_required
def credential_detail(request, pk):
    """View credential details"""
    credential = get_object_or_404(Credentials, pk=pk, user=request.user)
    
    # Update last accessed using business logic
    AccessTracker.update_access_time(credential, request.user)
    
    # Log activity
    ActivityManager.log_activity(
        request.user, 'view_credential', 
        f'Viewed credential: {credential.label}', request
    )
    
    context = {
        'credential': credential,
    }
    
    return render(request, 'frontend/credential_detail.html', context)


@login_required
def credential_create(request):
    """Create new credential"""
    if request.method == 'POST':
        # Use business logic to create credential
        credential, errors = CredentialsManager.create_credential(request.user, request.POST)
        
        if credential:
            # Log activity
            ActivityManager.log_activity(
                request.user, 'create_credential', 
                f'Created credential: {credential.label}', request
            )
            
            messages.success(request, f'Credential "{credential.label}" created successfully!')
            return redirect('frontend:credential_detail', pk=credential.pk)
        else:
            # Form has errors - recreate form with errors
            form = CredentialForm(request.POST)
            form.is_valid()  # Populate errors
    else:
        form = CredentialForm()
    
    context = {
        'form': form,
        'title': 'Add New Credential',
    }
    
    return render(request, 'frontend/credential_form.html', context)


@login_required
def credential_edit(request, pk):
    """Edit existing credential"""
    credential = get_object_or_404(Credentials, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Use business logic to update credential
        updated_credential, errors = CredentialsManager.update_credential(credential, request.POST)
        
        if updated_credential:
            # Log activity
            ActivityManager.log_activity(
                request.user, 'update_credential', 
                f'Updated credential: {updated_credential.label}', request
            )
            
            messages.success(request, f'Credential "{updated_credential.label}" updated successfully!')
            return redirect('frontend:credential_detail', pk=updated_credential.pk)
        else:
            # Form has errors - recreate form with errors
            form = CredentialForm(request.POST, instance=credential)
            form.is_valid()  # Populate errors
    else:
        form = CredentialForm(instance=credential)
    
    context = {
        'form': form,
        'credential': credential,
        'title': f'Edit {credential.label}',
    }
    
    return render(request, 'frontend/credential_form.html', context)


@login_required
@require_POST
def credential_delete(request, pk):
    """Delete credential"""
    credential = get_object_or_404(Credentials, pk=pk, user=request.user)
    
    # Use business logic to delete credential
    credential_label = CredentialsManager.delete_credential(credential)
    
    # Log activity
    ActivityManager.log_activity(
        request.user, 'delete_credential', 
        f'Deleted credential: {credential_label}', request
    )
    
    messages.success(request, f'Credential "{credential_label}" deleted successfully!')
    return redirect('frontend:credentials_list')


@login_required
def notes_list(request):
    """List all secure notes"""
    form = SearchManager.get_search_form(request.GET)
    
    # Get search parameters
    search_params = {}
    if form.is_valid():
        search_params = {
            'query': form.cleaned_data.get('query'),
            'favorites_only': form.cleaned_data.get('favorites_only'),
        }
    
    # Get notes using business logic
    notes = SecureNotesManager.get_user_notes(request.user, search_params)
    
    # Paginate results
    page_obj = PaginationManager.paginate_queryset(notes, request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'total_count': notes.count(),
    }
    
    return render(request, 'frontend/notes_list.html', context)


@login_required
def note_detail(request, pk):
    """View note details"""
    note = get_object_or_404(SecureNote, pk=pk, user=request.user)
    
    # Update last accessed using business logic
    AccessTracker.update_access_time(note, request.user)
    
    # Log activity
    ActivityManager.log_activity(
        request.user, 'view_note', 
        f'Viewed note: {note.title}', request
    )
    
    context = {
        'note': note,
    }
    
    return render(request, 'frontend/note_detail.html', context)


@login_required
def note_create(request):
    """Create new secure note"""
    if request.method == 'POST':
        # Use business logic to create note
        note, errors = SecureNotesManager.create_note(request.user, request.POST)
        
        if note:
            # Log activity
            ActivityManager.log_activity(
                request.user, 'create_note', 
                f'Created note: {note.title}', request
            )
            
            messages.success(request, f'Note "{note.title}" created successfully!')
            return redirect('frontend:note_detail', pk=note.pk)
        else:
            # Form has errors - recreate form with errors
            form = SecureNoteForm(request.POST)
            form.is_valid()  # Populate errors
    else:
        form = SecureNoteForm()
    
    context = {
        'form': form,
        'title': 'Add New Note',
    }
    
    return render(request, 'frontend/note_form.html', context)


@login_required
def note_edit(request, pk):
    """Edit existing note"""
    note = get_object_or_404(SecureNote, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Use business logic to update note
        updated_note, errors = SecureNotesManager.update_note(note, request.POST)
        
        if updated_note:
            # Log activity
            ActivityManager.log_activity(
                request.user, 'update_note', 
                f'Updated note: {updated_note.title}', request
            )
            
            messages.success(request, f'Note "{updated_note.title}" updated successfully!')
            return redirect('frontend:note_detail', pk=updated_note.pk)
        else:
            # Form has errors - recreate form with errors
            form = SecureNoteForm(request.POST, instance=note)
            form.is_valid()  # Populate errors
    else:
        form = SecureNoteForm(instance=note)
    
    context = {
        'form': form,
        'note': note,
        'title': f'Edit {note.title}',
    }
    
    return render(request, 'frontend/note_form.html', context)


@login_required
@require_POST
def note_delete(request, pk):
    """Delete note"""
    note = get_object_or_404(SecureNote, pk=pk, user=request.user)
    
    # Use business logic to delete note
    note_title = SecureNotesManager.delete_note(note)
    
    # Log activity
    ActivityManager.log_activity(
        request.user, 'delete_note', 
        f'Deleted note: {note_title}', request
    )
    
    messages.success(request, f'Note "{note_title}" deleted successfully!')
    return redirect('frontend:notes_list')


@login_required
@require_POST
def toggle_favorite(request):
    """Toggle favorite status for credential or note (AJAX endpoint)"""
    try:
        item_type = request.POST.get('type')
        item_id = request.POST.get('id')
        
        if item_type == 'credential':
            item = get_object_or_404(Credentials, pk=item_id, user=request.user)
        elif item_type == 'note':
            item = get_object_or_404(SecureNote, pk=item_id, user=request.user)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid type'})
        
        # Use business logic to toggle favorite
        is_favorite = FavoriteManager.toggle_favorite(item, request.user)
        
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def export_data(request):
    """Export user data as CSV"""
    # Use business logic to export data
    response = DataExportManager.export_user_data(request.user)
    
    # Log activity
    ActivityManager.log_activity(request.user, 'export_data', 'Exported user data', request)
    
    return response


@login_required
def search(request):
    """Search page with advanced filters"""
    form = SearchManager.get_search_form(request.GET)
    results = None
    
    if form.is_valid() and form.cleaned_data.get('query'):
        query = form.cleaned_data.get('query')
        type_filter = form.cleaned_data.get('type_filter')
        favorites_only = form.cleaned_data.get('favorites_only')
        
        # Use business logic to search
        results = SearchManager.search_all_user_data(
            request.user, query, type_filter, favorites_only
        )
        
        # Paginate results
        credentials_page = PaginationManager.paginate_queryset(
            results['credentials'], request.GET.get('cred_page')
        )
        notes_page = PaginationManager.paginate_queryset(
            results['notes'], request.GET.get('note_page')
        )
        
        results['credentials_page'] = credentials_page
        results['notes_page'] = notes_page
    
    context = {
        'form': form,
        'results': results,
    }
    
    return render(request, 'frontend/search.html', context)


@login_required
def activity_log(request):
    """View activity log"""
    activities = ActivityManager.get_user_activities(request.user, 100)
    
    # Paginate activities
    page_obj = PaginationManager.paginate_queryset(activities, request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'frontend/activity_log.html', context) 