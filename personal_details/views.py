# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views

# Models
from .models import User, SalaryTitleRecord, AcademicRecord, Spouse, EmploymentHistory
from django.db.models import Q
from django.forms.models import inlineformset_factory

# Form classes
from . import forms
from django.forms import HiddenInput

# Response
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Utils
from django_ajax.decorators import ajax
import datetime
from swhr import utils


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'personal_details.html'
    context_object_name = 'users'
    paginate_by = 13

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponseRedirect(reverse_lazy('personal_details:update_user', kwargs={'slug': self.request.user.slug}))
        return super().get(request)

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'last_name')
        if self.request.user.is_superuser:
            # Filtering
            staff_id = self.request.GET.get('staff_id', '')
            name = self.request.GET.get('name', '')
            is_active = bool(self.request.GET.get('is_active', 'True'))

            if bool(staff_id + name):
                print('Staff Filtering: %s %s %s' %
                      (staff_id, name, is_active))

                return User.objects.order_by(order_by).filter(Q(staff_id__contains=staff_id),
                                                              Q(last_name__contains=name)
                                                              | Q(first_name__contains=name) | Q(nick_name__contains=name),
                                                              Q(is_active=is_active),
                                                              Q(is_staff=False),)
            else:
                return User.objects.order_by(order_by).filter(Q(is_staff=False),)
        else:
            return User.objects.order_by(order_by).filter(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', 'last_name')

        # Filtering
        context['staff_id'] = self.request.GET.get('staff_id', '')
        context['name'] = self.request.GET.get('name', '')
        context['is_active'] = self.request.GET.get('is_active', 'True')

        context['is_active_options'] = dict(
            {'True': 'Active', '': 'Inactive'})

        context['filter'] = 'staff_id=%s&name=%s' % (
            context['staff_id'], context['name'], )

        return context


class UserCreateView(PermissionRequiredMixin, CreateView):
    form_class = forms.UserCreateForm
    model = User
    template_name = 'form_employee.html'
    permission_required = 'personal_details.create_user'
    AcademicRecordInlineFormset = inlineformset_factory(
        User, AcademicRecord,
        form=forms.AcademicRecordForm,
        can_delete=False,
        extra=1,
    )
    EmploymentHistoryInlineFormset = inlineformset_factory(
        User, EmploymentHistory,
        form=forms.EmploymentHistoryForm,
        can_delete=False,
        extra=1,
    )

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['ARFormset'] = self.AcademicRecordInlineFormset(
                self.request.POST,
                prefix='academicRecord'
            )
            context['ARFormsetHelper'] = forms.AcademicRecordFormsetHelper()

            context['EHFormset'] = self.EmploymentHistoryInlineFormset(
                self.request.POST,
                prefix='employmentHistory'
            )
            context['EHFormsetHelper'] = forms.EmploymentHistoryFormsetHelper()
        else:
            context['ARFormset'] = self.AcademicRecordInlineFormset(
                prefix='academicRecord'
            )
            context['ARFormsetHelper'] = forms.AcademicRecordFormsetHelper()

            context['EHFormset'] = self.EmploymentHistoryInlineFormset(
                prefix='employmentHistory'
            )
            context['EHFormsetHelper'] = forms.EmploymentHistoryFormsetHelper()
        return context

    def form_invalid(self, form):
        context = self.get_context_data()
        ARFormset = context['ARFormset']
        EHFormset = context['EHFormset']
        print("Form is valid if True: basic-%s, ARForm-%s, EHForm-%s" %
              (form.is_valid(), ARFormset.is_valid(), EHFormset.is_valid()))
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print('Validating Form')
        context = self.get_context_data()
        ARFormset = context['ARFormset']
        EHFormset = context['EHFormset']
        print("Form is valid if True: basic-%s, ARForm-%s, EHForm-%s" %
              (form.is_valid(), ARFormset.is_valid(), EHFormset.is_valid()))
        if form.is_valid() and ARFormset.is_valid() and EHFormset.is_valid():
            super().form_valid(form)  # Save User object
            data = form.cleaned_data
            user = User.objects.get(
                staff_id=data['staff_id'])

            # Spouse
            if data['marital_status'] != 'SI':
                try:
                    spouse = Spouse(
                        user=user, name=data['spouse_name'], identity_type=data['spouse_identity_type'], identity_no=data['spouse_identity_no'])
                    spouse.save()
                except Exception as e:
                    print('Something\'s wrong when creating spouse for %s' % user)

            # SalaryTitleRecord
            try:
                salary_title_record = SalaryTitleRecord(
                    date_changed=data['date_joined'], department=data['department'], salary=data['salary'], title=data['title'], grade=data['grade'], user=user)
                salary_title_record.save()
            except Exception as e:
                print(
                    'Something\'s wrong when creating salary title record for %s' % user)

            # AcademicRecord
            try:
                for f in ARFormset:
                    form_data = f.cleaned_data
                    if form_data:
                        academicRecord = AcademicRecord(date_start=form_data['date_start'], date_end=form_data['date_end'], institution_name=form_data[
                                                        'institution_name'], qualification=form_data['qualification'], year_completed=form_data['year_completed'], user=user)
                        academicRecord.save()
                        print(academicRecord)
            except Exception as e:
                print(
                    'Something\'s wrong when creating academic record for %s' % user)

            try:
                for f in EHFormset:
                    form_data = f.cleaned_data
                    if form_data:
                        employmentHistory = EmploymentHistory(date_start=form_data['date_start'], date_end=form_data['date_end'], employer_name=form_data[
                            'employer_name'], position=form_data['position'], reason=form_data['reason'], user=user)
                        employmentHistory.save()
                        print(employmentHistory)
            except Exception as e:
                print(
                    'Something\'s wrong when creating employment history record for %s' % user)

            return HttpResponseRedirect(reverse_lazy('personal_details:index'))

        print('Something\'s wrong with form validation')
        return self.render_to_response(self.get_context_data(form=form))


class UserUpdateView(UserPassesTestMixin, UpdateView):
    form_class = forms.UserUpdateForm
    model = User
    slug = 'staff_id'
    template_name = 'form_employee.html'
    AcademicRecordInlineFormset = inlineformset_factory(
        User, AcademicRecord,
        form=forms.AcademicRecordForm,
        can_delete=True,
        extra=1,
        widgets={
            'DELETE': HiddenInput(),
        }
    )
    EmploymentHistoryInlineFormset = inlineformset_factory(
        User, EmploymentHistory,
        form=forms.EmploymentHistoryForm,
        can_delete=True,
        extra=1,
        widgets={
            'DELETE': HiddenInput(),
        }
    )
    SalaryTitleRecordInlineFormset = inlineformset_factory(
        User, SalaryTitleRecord,
        form=forms.SalaryTitleRecordForm,
        can_delete=False,
        extra=0,
    )

    def test_func(self):
        user = self.get_object()
        return (user.slug == self.request.user.slug and user.is_active) or self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            user = self.get_object()
            context['ARFormset'] = self.AcademicRecordInlineFormset(
                self.request.POST, instance=user, prefix='academicRecord')
            context['ARFormsetHelper'] = forms.AcademicRecordFormsetHelper()

            context['EHFormset'] = self.EmploymentHistoryInlineFormset(
                self.request.POST, instance=user, prefix='employmentHistory')
            context['EHFormsetHelper'] = forms.EmploymentHistoryFormsetHelper()
        else:
            user = self.get_object()
            context['ARFormset'] = self.AcademicRecordInlineFormset(
                instance=user,
                prefix='academicRecord'
            )
            context['ARFormsetHelper'] = forms.AcademicRecordFormsetHelper()

            context['EHFormset'] = self.EmploymentHistoryInlineFormset(
                instance=user,
                prefix='employmentHistory'
            )
            context['EHFormsetHelper'] = forms.EmploymentHistoryFormsetHelper()
            context['STFormset'] = self.SalaryTitleRecordInlineFormset(
                instance=user,
            )
            context['STFormsetHelper'] = forms.SalaryTitleRecordFormsetHelper()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ARFormset = context['ARFormset']
        EHFormset = context['EHFormset']
        if form.is_valid() and ARFormset.is_valid() and EHFormset.is_valid():
            user = self.get_object()
            data = form.cleaned_data
            if data['department'] != user.department or data['title'] != user.title or data['salary'] != user.salary or data['grade'] != user.grade:
                salary_title_record = SalaryTitleRecord(
                    date_changed=datetime.date.today(), department=data['department'], salary=data['salary'], title=data['title'], grade=data['grade'], user=user)
                try:
                    salary_title_record.save()
                except Exception as e:
                    print('Error with salary title record update.')
            super().form_valid(form)  # Save User object
            try:
                ARFormset.save()
            except Exception as e:
                print('Error with AR Form')
            try:
                EHFormset.save()
            except Exception as e:
                print('Error with EH Form')
            return HttpResponseRedirect(reverse_lazy('personal_details:index'))
        return self.render_to_response(self.get_context_data(form=form))


@ajax
def annual_leave_calculation(request):
    date_joined = datetime.datetime.strptime(
        request.GET['date_joined'], '%Y-%m-%d').date()
    annual_leave = utils.annual_leave_to_year_end(date_joined)
    return {'annual_leave': annual_leave}
