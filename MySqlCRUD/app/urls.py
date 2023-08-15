from django.urls import path 
from . import emp_views, dept_views

urlpatterns = [
    
    # ------------------- Employee --------------------
    path('list-employee', emp_views.get_employees, name='list-employees'), 
    path('create-employee', emp_views.create_employees, name='create-employees'), 
    path('update-employee/<int:emp_id>', emp_views.update_employees, name='update-employees'), 
    path('delete-employee/<int:emp_id>', emp_views.delete_employees, name='delete-employees'), 
    
    # -------------------- Dept ------------------------
    path('list-Dept', dept_views.get_dept, name='list-Dept'), 
    path('create-Dept', dept_views.create_dept, name='create-Dept'), 
    path('update-Dept/<int:dept_id>', dept_views.update_dept, name='update-Dept'), 
    path('delete-Dept/<int:dept_id>', dept_views.delete_dept, name='delete-Dept'), 
    
    # -------------------- Search ----------------------
    
    path('search-employee', emp_views.search_employees, name='search_employees'),
    path('search-dept', dept_views.search_dept, name='search_dept'),
    
    path('search-dept-in-dept', dept_views.search_emp_in_dept, name='search_emp_in_dept'),
    path('search-emp-in-dept', emp_views.search_emp_dept, name='search_emp_in_dept'),
    
    
]

