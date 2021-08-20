from ascuv_emulator.celery import app
from providers.models import Provider, ProviderValue
from providers.services.provider_services import ProviderService
from providers.services.values_services import UpdateValuesService, HttpSendValuesService


@app.task
def provider_creation_task():
    ProviderService().create_provider()
    return True


@app.task
def provider_values_creation_task():
    providers = Provider.objects.all()
    service = UpdateValuesService()
    for provider in providers:
        service.build_new_value(provider)
    return True


@app.task
def send_data(value_id):
    HttpSendValuesService('http://vodomer:8000/core/receive/')\
        .send_value(ProviderValue.objects.select_related('provider__client').get(id=value_id))


@app.task
def process_values_sending():
    for value_id in ProviderValue.objects.filter(sent_at__isnull=True).values_list('id', flat=True):
        send_data.apply_async(args=(value_id, ))
