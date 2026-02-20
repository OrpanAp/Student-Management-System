from django.shortcuts import render, reverse, redirect
from django.views import generic
from django.db.models import Q
from django.contrib.auth import mixins as auth_mixins
from . import mixins
from . import forms
from . import models
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
import datetime
import random


class UserListView(mixins.StaffRequiredMixin, generic.ListView):
    template_name = "users/user_list.html"
    context_object_name = 'users'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = models.User.objects.filter(is_superuser=False)
        
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(role__icontains=search)
            )
            
        return queryset

class UserCreateView(generic.CreateView):
    template_name = "accounts/user_create.html"
    form_class = forms.UserCreateForm

    def form_valid(self, form):
        user_form = form.save(commit=False)
        user_form.save() 
        
        user_form.username = f'{user_form.first_name}{user_form.last_name}{user_form.id}'
        user_form.save()
        
        self.role = form.cleaned_data['role']
        return super(UserCreateView, self).form_valid(form)
    
    def get_success_url(self):
        if self.role == 'Student':
            return reverse('accounts:student_class', kwargs={'pk': self.object.pk})
        
        return reverse('home')
    
class UserDeleteView(mixins.StaffRequiredMixin, generic.DeleteView):
    template_name = "accounts/user_delete.html"
    
    def get_queryset(self):
        return models.User.objects.filter(is_superuser=False)
    
    def get_success_url(self):
        return reverse('accounts:user_list')

class UserDetailView(mixins.StaffRequiredMixin, generic.DetailView):
    template_name = "accounts/user_detail.html"
    context_object_name = 'user'

    def get_queryset(self):
        queryset = models.User.objects.all()
        return queryset
    
class UserUpdateView(mixins.StaffRequiredMixin, generic.UpdateView):
    template_name = "accounts/update_user.html"
    form_class = forms.UpdateAccountForm
    
    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('pk')
        
        queryset = get_object_or_404(models.User, pk=user_pk, is_superuser=False)
        self.role = queryset.role
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.object
        context["form_type"] = "user"

        return context
    
    def form_valid(self, form):
        user_form = form.save(commit=False)
        user_form.save()
        self.role = form.cleaned_data.get("role")
        return super(UserUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        if self.role == 'Student':
            return reverse('accounts:student_class', kwargs={'pk': self.object.pk})
        
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})



class StudentListView(mixins.StaffRequiredMixin, generic.ListView):
    template_name = "students/student_list.html"
    context_object_name = 'students'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_choices'] = sorted(
            models.StudentProfile.objects.values_list('class_list', flat=True).distinct(),
            key=lambda x: int(x)  # convert string to int for correct numeric order
        )
        return context

    
    def get_queryset(self):
        queryset = models.User.objects.filter(role='Student').select_related('studentprofile')
        
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(studentclass__class_list__icontains=search) |
                Q(studentclass__roll__icontains=search)
            )
            
        category_filter = self.request.GET.get('class')
        
        if category_filter:
            queryset = queryset.filter(studentclass__class_list=category_filter)
            
        return queryset
    
class StudentCreateView(mixins.StaffRequiredMixin, generic.CreateView):
    template_name = "students/student_create.html"
    form_class = forms.StudentCreateForm

    def form_valid(self, form):
        student_form = form.save(commit=False)
        student_form.save() 
        
        student_form.role = 'Student'
        student_form.username = f'{student_form.first_name}{student_form.last_name}{student_form.id}'
        student_form.set_password(f'{random.randint(0, 1000000)}')
        student_form.save()
        
        return super(StudentCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('accounts:student_class', kwargs={'pk': self.object.pk})

class StudentClassView(mixins.StaffRequiredMixin, generic.CreateView):
    template_name = "students/student_class.html"
    form_class = forms.StudentClassAssignForm
    
    def form_valid(self, form):
        student_pk = self.kwargs.get('pk')
        user = models.User.objects.get(pk=student_pk)

        student_class = form.save(commit=False)
        student_class.user = user
        
        class_at = form.cleaned_data['class_list']
        
        current_year = datetime.datetime.now().year
        count = models.StudentProfile.objects.filter(user__role='Student', class_list=class_at).count() + 1
        student_class.roll = f'{current_year}{class_at}{count}'
        
        student_class.save()

        return super(StudentClassView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('accounts:student_list')
    
class StudentDetailView(mixins.StaffRequiredMixin, generic.DetailView):
    template_name = "students/student_detail.html"
    context_object_name = 'student'

    def get_queryset(self):
        queryset = models.User.objects.filter(role='Student')
        return queryset
    
class StudentAccountUpdateView(mixins.StaffRequiredMixin, generic.UpdateView):
    template_name = "students/student_update_user.html"
    form_class = forms.UpdateAccountForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'user'):  # For StudentClassUpdateView
            context['student'] = self.object.user
        else:
            context['student'] = self.object  # For User update
        context['form_type'] = 'user'
        return context

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('pk')
        # Safely get the user with role 'Student'
        return get_object_or_404(models.User, pk=user_pk, role='Student')

    def get_success_url(self):
        return reverse('accounts:student_detail', kwargs={'pk': self.object.pk})
    
class StudentClassUpdateView(mixins.StaffRequiredMixin, generic.UpdateView):
    template_name = "students/student_update_class.html"
    form_class = forms.StudentUpdateClassAssignForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'user'):  # For StudentClassUpdateView
            context['student'] = self.object.user
        else:
            context['student'] = self.object  # For User update
        context['form_type'] = 'class'
        return context

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('pk')
        return get_object_or_404(models.StudentProfile, user__pk=user_pk)

    def get_success_url(self):
        return reverse('accounts:student_detail', kwargs={'pk': self.object.user.pk})
 
 
class StudentDeleteView(mixins.StaffRequiredMixin, generic.DeleteView):
    template_name = "students/student_delete.html"
    
    def get_queryset(self):
        return models.User.objects.filter(role='Student')
    
    def get_success_url(self):
        return reverse('accounts:student_list')
    
class StudentAddResultView(mixins.StaffRequiredMixin, generic.CreateView):
    template_name = "students/student_add_result.html"
    form_class = forms.StudentAddResult
    
    def get_success_url(self):
        return reverse('home')

class StudentAddAttendanceView(mixins.StaffRequiredMixin, generic.CreateView):
    template_name = "students/student_add_result.html"
    form_class = forms.StudentAddAttandance
    
    def get_success_url(self):
        return reverse('home')

    
class StudentResultListView( generic.ListView):
    template_name = "students/student_result_list.html"
    context_object_name = 'results'
    
    def dispatch(self, request, *args, **kwargs):
        # If the user is anonymous, redirect to home
        user_role = getattr(request.user, 'role', 'Guest')
        if user_role == 'Guest':
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = models.StudentResult.objects.select_related(
            "user",
            "user__studentprofile"
        )

        user_role = getattr(self.request.user, 'role', 'Guest')

        if user_role == 'Student':
            queryset = queryset.filter(user=self.request.user)

        # 🔎 FILTERS

        year_filter = self.request.GET.get('year')
        if year_filter:
            queryset = queryset.filter(year=year_filter)

        semester_filter = self.request.GET.get('semester')
        if semester_filter:
            queryset = queryset.filter(semester=semester_filter)

        class_filter = self.request.GET.get('class')
        if class_filter:
            queryset = queryset.filter(
                user__studentprofile__class_list=class_filter
            )
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(user__studentprofile__roll__icontains=search)
            )

        return queryset.order_by('-year', 'semester')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = context['results']

        grouped_results = {}

        for result in queryset:
            year = result.year
            semester = result.semester

            if year not in grouped_results:
                grouped_results[year] = {}

            if semester not in grouped_results[year]:
                grouped_results[year][semester] = []

            grouped_results[year][semester].append(result)

        context['grouped_results'] = grouped_results

        # For filter dropdowns
        all_results = models.StudentResult.objects.all()

        context['years'] = all_results.values_list('year', flat=True).distinct()
        context['semesters'] = all_results.values_list('semester', flat=True).distinct()
        context['classes'] = all_results.values_list(
            'user__studentprofile__class_list',
            flat=True
        ).distinct()

        context['selected_year'] = self.request.GET.get('year', '')
        context['selected_semester'] = self.request.GET.get('semester', '')
        context['selected_class'] = self.request.GET.get('class', '')

        return context
    
    def get_template_names(self):
        if self.request.user.role == 'Student':
            return ["students/student_result_list.html"]
        elif self.request.user.is_staff:
            return ["students/student_result_list_staff_site.html"]
        return super().get_template_names()
    
class StudentResultDeleteView(mixins.StaffRequiredMixin, generic.DeleteView):
    template_name = "students/student_result_delete.html"
    context_object_name = 'student'
    
    def get_queryset(self):
        return models.StudentResult.objects.all()
    
    def get_success_url(self):
        return reverse('accounts:student_result_list')
    
    
class StudentResultUpdateView(mixins.StaffRequiredMixin, generic.UpdateView):
    template_name = "students/student_update_result.html"
    form_class = forms.StudentResultUpdate
    
    def get_queryset(self):
        return models.StudentResult.objects.all()
    
    def get_success_url(self):
        return reverse('accounts:student_result_list')
    
    


     