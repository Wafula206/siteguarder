import requests
import json
from django.shortcuts import render
from .forms import ScanForm
from .models import ScanResult

SECURITY_HEADERS = [
    'Content-Security-Policy',
    'X-Frame-Options',
    'Strict-Transport-Security',
    'X-Content-Type-Options',
    'Referrer-Policy',
    'Permissions-Policy',
]

HEADER_DESCRIPTIONS = {
    'Content-Security-Policy': 'Helps prevent XSS attacks by specifying which dynamic resources are allowed to load.',
    'X-Frame-Options': 'Protects against clickjacking by controlling whether your site can be framed.',
    'Strict-Transport-Security': 'Forces browsers to use HTTPS, protecting against man-in-the-middle attacks.',
    'X-Content-Type-Options': 'Prevents browsers from MIME-sniffing a response away from the declared content-type.',
    'Referrer-Policy': 'Controls how much referrer information is included with requests.',
    'Permissions-Policy': 'Allows or denies use of browser features in the site’s context.',
}

def home_view(request):
    return render(request, 'scanner/home.html')

def about_view(request):
    return render(request, 'scanner/about.html')

def scan_view(request):
    result = None
    missing = []
    headers = {}
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            if not url.startswith("http"):
                url = "https://" + url
            try:
                response = requests.get(url, timeout=5, allow_redirects=True)
                headers = response.headers
                missing = [h for h in SECURITY_HEADERS if h not in headers]
                result = {
                    'url': url,
                    'headers': headers,
                    'missing': missing,
                }
                # Save scan result to the database
                ScanResult.objects.create(
                    url=url,
                    is_https=url.startswith('https'),
                    missing_headers=json.dumps(missing),
                    all_headers=dict(headers)
                )
            except Exception as e:
                result = {'error': str(e)}
    else:
        form = ScanForm()
    return render(
        request,
        'scanner/scan.html',
        {'form': form, 'result': result, 'header_descriptions': HEADER_DESCRIPTIONS}
    )

def history_view(request):
    scans = ScanResult.objects.order_by('-scan_time')[:20]
    # Parse missing_headers JSON for each scan for template use
    for scan in scans:
        try:
            scan.missing_headers_list = json.loads(scan.missing_headers)
        except Exception:
            scan.missing_headers_list = []
    return render(request, 'scanner/history.html', {'scans': scans})