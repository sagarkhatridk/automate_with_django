from django.shortcuts import render
from .utils import get_all_custom_models
from uploads.models import Upload
from django.shortcuts import redirect
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

def import_data(request):
    if request.method == "POST":
        file_path = request.FILES['file_path']
        model_name = request.POST['model_name']

        # store this file inside the Upload Model.
        upload = Upload.objects.create(
            file=file_path,
            model_name=model_name
        )

        # constuct the full path
        base_url = str(settings.BASE_DIR)
        relative_path = str(upload.file.url)

        file_path = base_url + relative_path

        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, 'Data Imported Successfully.')
        except Exception as E:
            messages.error(request, str(E))

        # trigger the importdata command

        return redirect('import_data')

    else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models':custom_models
        }
    return render(request, 'dataentry/importdata.html', context)