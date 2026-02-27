from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Names
from .forms import MemberForm, MemberSearchForm
from .emails import send_welcome_email, send_member_update_notification, send_deletion_confirmation

# Create your views here.
def members(request):
    """
    Display list of members with optional search/filter.
    """
    mymembers = Names.objects.all()
    
    # Handle search form
    search_form = MemberSearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_query')
        status_filter = search_form.cleaned_data.get('status_filter')
        
        if search_query:
            mymembers = mymembers.filter(
                firstname__icontains=search_query
            ) | mymembers.filter(
                lastname__icontains=search_query
            ) | mymembers.filter(
                city__icontains=search_query
            ) | mymembers.filter(
                location__icontains=search_query
            )
        
        if status_filter:
            mymembers = mymembers.filter(status=status_filter)
    
    paginator = Paginator(mymembers, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.page(page_number)

    return render(request, 'first.html', {
        'page': page,
        'search_form': search_form,
    })

def details(request, slug):
    """
    Display member details.
    """
    mymember = get_object_or_404(Names, slug=slug)
    return render(request, 'details.html', {'mymember': mymember})

def main(request):
    """
    Display homepage.
    """
    return render(request, 'main.html')

def testing(request):
    """
    Testing page.
    """
    context = {'fruits': ["banana", "apple", "oranges"]}
    return render(request, 'test.html', context)

def create_member(request):
    """
    Create a new member using ModelForm.
    
    This view handles both GET (display form) and POST (process form) requests.
    When a member is successfully created, a welcome email is automatically sent.
    
    IMPORTANT: For file uploads, form must include request.FILES
    """
    if request.method == 'POST':
        # POST request: User submitted the form
        # request.FILES contains uploaded files
        # MUST pass both request.POST and request.FILES for file uploads
        form = MemberForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Form validation passed
            # Save the form data to create a new member
            # This automatically handles file upload
            member = form.save()
            
            # Send welcome email to the new member
            email_sent = send_welcome_email(member)
            
            # Add success message
            if email_sent:
                messages.success(
                    request, 
                    f'Member {member.firstname} {member.lastname} created successfully! '
                    f'A welcome email has been sent to {member.email}.'
                )
            else:
                messages.success(
                    request, 
                    f'Member {member.firstname} {member.lastname} created successfully!'
                )
                messages.warning(
                    request,
                    'However, the welcome email could not be sent. Please check email configuration.'
                )
            
            # Redirect to member detail page
            return redirect('club:member-detail', slug=member.slug)
        else:
            # Form validation failed
            # Django will automatically display errors in the template
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        # GET request: Display empty form
        form = MemberForm()
    
    return render(request, 'create_member.html', {'form': form})

def edit_member(request, slug):
    """
    Edit an existing member using ModelForm.
    
    This demonstrates how to use ModelForm for updating existing records.
    Sends a notification email when member information is updated.
    
    IMPORTANT: For file uploads, form must include request.FILES
    """
    # Get the member or return 404
    member = get_object_or_404(Names, slug=slug)
    
    if request.method == 'POST':
        # POST request: User submitted the form
        # Pass the instance to populate form with existing data
        # MUST include request.FILES for file uploads
        form = MemberForm(request.POST, request.FILES, instance=member)
        
        if form.is_valid():
            # Delete old profile picture if new one is uploaded
            if 'profile_picture' in request.FILES:
                from .file_utils import delete_old_profile_picture
                delete_old_profile_picture(member)
            
            # Save updates to the existing member
            updated_member = form.save()
            
            # Send update notification email
            email_sent = send_member_update_notification(updated_member)
            
            if email_sent:
                messages.success(
                    request,
                    f'Member {updated_member.firstname} {updated_member.lastname} updated successfully! '
                    f'A notification email has been sent.'
                )
            else:
                messages.success(
                    request,
                    f'Member {updated_member.firstname} {updated_member.lastname} updated successfully!'
                )
            
            return redirect('club:member-detail', slug=updated_member.slug)
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        # GET request: Display form with existing data
        form = MemberForm(instance=member)
    
    return render(request, 'edit_member.html', {
        'form': form,
        'member': member,
    })

def delete_member(request, slug):
    """
    Delete a member with confirmation.
    Sends a deletion confirmation email before removing the member.
    """
    member = get_object_or_404(Names, slug=slug)
    
    if request.method == 'POST':
        # User confirmed deletion
        member_name = f"{member.firstname} {member.lastname}"
        member_email = member.email
        
        # Send deletion confirmation email before deleting
        send_deletion_confirmation(member_email, member_name)
        
        # Delete the member
        member.delete()
        
        messages.success(
            request,
            f'Member {member_name} deleted successfully. A confirmation email has been sent.'
        )
        
        return redirect('club:members')
    
    # GET request: Show confirmation page
    return render(request, 'delete_member.html', {'member': member})

# Custom error handlers
def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 error handler"""
    return render(request, '500.html', status=500)
