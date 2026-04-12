from django.shortcuts import render, redirect
from utils.auth import api_login_required
from utils.api_client import APIClient
from config.api_config import CUSTOMER_URL
from django.contrib import messages


@api_login_required
def customer_list(request):
    response = APIClient().get(CUSTOMER_URL)

    customers = []
    if response.status_code == 200:
        customers = response.json().get("data", [])

    return render(request, 'customers/list.html', {'customers': customers})


@api_login_required
def customer_create(request):
    if request.method == 'POST':
        data = {
            "name": request.POST.get('name'),
            "email": request.POST.get('email'),
            "phone": request.POST.get('phone')
        }

        response = APIClient().post(CUSTOMER_URL, data)
        res = response.json()
        msg = res.get("message", "Done")

        if res.get("status") == "success":
            messages.success(request, msg)
        else:
            messages.error(request, msg)

        return redirect('customer_list')

    return render(request, 'customers/form.html')


@api_login_required
def customer_update(request, pk):
    client = APIClient()

    #GET → load data into form
    if request.method == 'GET':
        response = client.get(CUSTOMER_URL, extra_headers={"id": str(pk)})

        customer = {}
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                customer = data[0]

        return render(request, 'customers/form.html', {'customer': customer})

    #POST → update
    if request.method == 'POST':
        data = {
            "id": int(pk),
            "name": request.POST.get('name'),
            "email": request.POST.get('email'),
            "phone": request.POST.get('phone')
        }

        response = client.put(CUSTOMER_URL, data)

        try:
            res = response.json()
            msg = res.get("message", "Something happened")
        except:
            msg = "Invalid API response"

        if response.status_code == 200 and res.get("status") == "success":
            messages.success(request, msg)
        else:
            messages.error(request, msg)

        return redirect('customer_list')


@api_login_required
def customer_delete(request, pk):
    response = APIClient().delete(CUSTOMER_URL, {"id": int(pk)})
    res = response.json()
    msg = res.get("message", "Done")

    if res.get("status") == "success":
        messages.success(request, msg)
    else:
        messages.error(request, msg)
        
    return redirect('customer_list')

@api_login_required
def customer_details(request, pk):
    client = APIClient()

    response = client.get(CUSTOMER_URL, extra_headers={"id": str(pk)})
    res = response.json()

    customer = {}
    if response.status_code == 200 and res.get("data"):
        data = res.get("data", [0])
        if data:
            customer = data[0]
    else:
        msg = res.get("message", "Done")
        messages.error(request, msg)

    return render(request, 'customers/profile.html', {'customer_profile': customer})
