from django.shortcuts import render, get_object_or_404
from .models import Employee

# Create your views here.
def index(request):
    employees = Employee.objects.all()
    context = {'employees': employees}
    return render(request, 'index.html', context)

def detail(request, staff_no):
    employee = get_object_or_404(Employee, pk = staff_no)
    if request.method == 'POST':
        employee.staff_no = request.POST['staff_no']
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.start_date = request.POST['start_date']
        employee.salary = request.POST['salary']
        employee.department = request.POST['department']
        employee.address = request.POST['address']
        employee.phone_no = request.POST['phone_no']
        employee.email = request.POST['email']
        employee.annual_leave = request.POST['annual_leave']
        return index(request)
    elif request.method == 'GET':
        context = {'employee': employee}
        return render(request, 'detail.html', context)

def new_staff(request):
    return render(request, 'new_staff.html')

def edit_staff(request, staff_no):
    return
