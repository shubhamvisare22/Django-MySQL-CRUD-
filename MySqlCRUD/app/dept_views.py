from django.http import JsonResponse
from .models import  Department, Employee
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# -------------------------- Department -----------------------------

@csrf_exempt
def get_dept(request):
    if request.method != "GET":
        return JsonResponse({"msg": "Invalid Request Method"})
    
    dept_obj = Department.objects.all().values()
    return JsonResponse({'data': list(dept_obj)})
    


@csrf_exempt
def create_dept(request):
    if request.method != 'POST':
        return JsonResponse({"msg": "Invalid Request Method"})
    
    name = request.POST.get('name')
    if not name or Department.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Department name already exists or Name is not given.'}, status=400)
    
    dept_obj = Department.objects.create(name=name)
    return JsonResponse({'msg': 'dept created', 'data': {'name': dept_obj.name, 'id': dept_obj.id}})


@csrf_exempt
def update_dept(request, dept_id):
    dept_obj = Department.objects.get(id=dept_id)
    
    if request.method == 'POST':
        return JsonResponse({"msg": "Invalid Request Method"})
    
    name = request.POST.get("name")
    if not name or Department.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Department name already exists or Name is not given.'}, status=400)
    
    dept_obj.name = name
    dept_obj.save()
    return JsonResponse({'data': {'Updated Name': dept_obj.name}})


@csrf_exempt
def delete_dept(request, dept_id):
    try:
        dept_obj = Department.objects.get(id=dept_id)
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Employee does not exist.'}, status=404)

    if request.method != 'POST':
        return JsonResponse({"msg": "Invalid Request Method"})
    
    dept_obj.delete()
    return JsonResponse({'msg': 'Record Deleted'})


def search_dept(request):
    # sourcery skip: assign-if-exp, reintroduce-else, swap-if-else-branches, use-named-expression
    search_query = request.GET.get('search')
    
    if not search_query:
        return JsonResponse({'msg':'Enter The Department Name to search'})
    
    if search_result := Department.objects.filter(name__icontains=str(search_query).strip()):
        return JsonResponse({'msg':'Matching Department Found', 'data':list(search_result.values())})
    
    return JsonResponse({'msg':'No Match Found'}) 
        
    
def search_emp_in_dept(request):
    search_query = request.GET.get('search')
    
    if not search_query:
        return JsonResponse({'msg':'Enter The Department Name to search'})
    
    if search_result := Department.objects.filter(name__icontains=str(search_query).strip()):
        lst = list(search_result.values())
        emp_obj = [list(Employee.objects.filter(dept=i['id']).values()) for i in lst]
        return JsonResponse({'msg':'Matching Department Found', 'data':list(search_result.values()), 'Employees':list(emp_obj)})
        
    return JsonResponse({'msg':'No Match Found'})
    
    

