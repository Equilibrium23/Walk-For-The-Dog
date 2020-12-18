from django.shortcuts import render
from django.db import connection

def start_page(request):
	#close_old_connections()
	return render(request,'start_page/start_page.html')

