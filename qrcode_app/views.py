from django.shortcuts import render
import os
from django.conf import settings
from .forms import QRCodeForm
import qrcode as QRC
from django.contrib import messages

def generate_qr_code(request):
    """
    Generate QR code based on the provided URL.
    """

    if request.method == 'POST':
        form = QRCodeForm(request.POST)

        if form.is_valid():
            restaurant_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']

            # Generate QR code using the restaurant name and URL
            try:
                qr = QRC.make(url)
                file_name = restaurant_name.replace(" ", "_").lower() + "_menu.png"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                qr.save(file_path)

                # Create image URL
                qr_url = os.path.join(settings.MEDIA_URL, file_name)

                messages.success(request, "QR Code generated successfully.")

            except Exception as E:
                qr_url = None
                file_name = None
                messages.error(request, f"Failed to generate QR code: {str(E)}")

            context = {
                    'restaurant_name': restaurant_name,
                    'qr_url': qr_url,
                    "file_name": file_name
            }

            return render(request, 'qr/qr_result.html', context)

    else:

        form = QRCodeForm()

        context = {
            'form': form,
        }

        return render(request, 'qr/generate_qr_code.html', context)
