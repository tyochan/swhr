from django import forms

class EmployeeForm(forms.Form):
    staff_no = CharField()
    first_name = CharField()
    last_name = CharField()
    start_date = models.DateField()
    salary = models.FloatField(default = 20000)
    address = models.CharField(max_length = 100, default = 'Kowloon, Hong Kong')
    phone_no = models.CharField(max_length = 20, default = '+852-65564053')
    annual_leave = models.DecimalField(max_digits = 3, decimal_places = 0, default = 12)
    email = models.EmailField(default = 'test@81.com')
    bank_acc = models.CharField(max_length = 100, default = '123-456-778')
    department = models.CharField(max_length = 100, default = '-')
