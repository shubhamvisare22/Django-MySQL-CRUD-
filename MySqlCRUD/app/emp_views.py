from django.http import JsonResponse
from .models import Employee, Department
from .emp_validations import validate_employee_data
from django.views.decorators.csrf import csrf_exempt


# ------------------- Employee --------------------------
@csrf_exempt
def get_employees(request):
    if request.method != "GET":
        return JsonResponse({"msg": "Invalid Request Method"})

    emp_obj = Employee.objects.all().values()
    return JsonResponse({'data': list(emp_obj)})


@csrf_exempt
def create_employees(request):
    if request.method != 'POST':
        return JsonResponse({"msg": "Invalid Request Method"})

    data = {
        'name': request.POST.get('name'),
        'age': request.POST.get('age'),
        'email': request.POST.get('email'),
        'salary': request.POST.get('salary'),
        'dept_name': request.POST.get('dept')
    }

    if errors := validate_employee_data(data):
        return JsonResponse({'errors': errors}, status=400)

    email = data['email']
    if Employee.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Employee with this email already exists.'}, status=400)

    dept_name = data['dept_name']
    try:
        department = Department.objects.get(name__iexact=dept_name)
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Department does not exist.'}, status=400)

    emp_obj = Employee.objects.create(
        name=data['name'], age=data['age'], email=email,
        salary=data['salary'], dept=department
    )

    return JsonResponse({'msg': 'Record Saved', 'data': {'id': emp_obj.id, 'name': emp_obj.name, 'dept': emp_obj.dept.name}})



@csrf_exempt
def update_employees(request, emp_id):
    emp_obj = Employee.objects.get(id=emp_id)
    if request.method != 'POST':
        return JsonResponse({"msg": "Invalid Request Method"})

    data = {
        'name': request.POST.get('name'),
        'age': request.POST.get('age'),
        'email': request.POST.get('email'),
        'salary': request.POST.get('salary'),
        'dept': request.POST.get('Department')
    }
    if errors := validate_employee_data(data):
        return JsonResponse({'errors': errors}, status=400)

    emp_obj.name = data['name']
    emp_obj.age = data['age']
    emp_obj.email = data['email']
    emp_obj.salary = data['salary']
    emp_obj.dept = data['dept']
    emp_obj.save()

    return JsonResponse({'data': list(emp_obj)})


@csrf_exempt
def delete_employees(request, emp_id):

    if request.method != 'POST':
        return JsonResponse({"msg": "Invalid Request Method"})

    try:
        emp_obj = Employee.objects.get(id=emp_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee does not exist.'}, status=404)

    emp_obj.delete()
    
    return JsonResponse({'msg': 'Record Deleted'})


def search_employees(request):
    # sourcery skip: assign-if-exp, reintroduce-else, swap-if-else-branches, use-named-expression
    search_query = request.GET.get('search')
    if not search_query:
        return JsonResponse({'error': 'Enter the Employee Name to Search.'})

    if search_result := Employee.objects.filter(name__icontains=str(search_query).strip()):
        return JsonResponse({'data': list(search_result.values())})
    
    return JsonResponse({'msg': 'No Match Found for the Employee '})

def search_emp_dept(request):
    search_query = request.GET.get('search')
    if not search_query:
        return JsonResponse({'error': 'Enter the Employee Name to Search.'})
    
    if search_result := Employee.objects.filter(name__icontains=str(search_query).strip()):
        lst = list(search_result.values())
        dept_obj = [list(Department.objects.filter(id=i['id']).values()) for i in lst]
        return JsonResponse({'data': list(search_result.values()), 'Department':dept_obj})

    return JsonResponse({'msg': 'No Match Found for the Employee '})
    
    