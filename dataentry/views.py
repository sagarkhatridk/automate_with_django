from django.shortcuts import render
from .utils import check_csv_function, get_all_custom_models
from uploads.models import Upload
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from .tasks import import_data_task, export_data_task
from django.core.management import call_command


def import_data(request):
    if request.method == "POST":
        file_path = request.FILES["file_path"]
        model_name = request.POST["model_name"]

        # store this file inside the Upload Model.
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # constuct the full path
        base_url = str(settings.BASE_DIR)
        relative_path = str(upload.file.url)

        file_path = base_url + relative_path

        try:
            check_csv_function(file_path, model_name)
        except Exception as E:
            messages.error(request, str(E))
            return redirect("import_data")

        # handle the import data task
        import_data_task.delay(file_path, model_name)

        messages.success(
            request,
            "Your data is being imported, \n You will be notified once it will be done.",
        )
        return redirect("import_data")

    else:
        custom_models = get_all_custom_models()
        context = {"custom_models": custom_models}
    return render(request, "dataentry/importdata.html", context)


def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get("model_name")
        export_data_task.delay(model_name)
        messages.success(
            request,
            "Your data is being exported \n You will be notified once it will be done.",
        )
        return redirect("export_data")
    else:
        custom_models = get_all_custom_models()
        context = {"custom_models": custom_models}
    return render(request, "dataentry/exportdata.html", context)
