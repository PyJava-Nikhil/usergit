from celery import task
from accounts.models import Account, APIReport
import json
import traceback
from django.utils import timezone
#Create your tasks here or other utils

def bytes_to_json(byte_data):
    data = byte_data.decode("utf-8").replace("'", '"')
    json_data = json.loads(data)
    return json_data

@task()
def create_update_user(user_data, url):
    try:
        for data in user_data:
            account_obj, account_created = Account.objects.update_or_create(
                login = data["login"],
                unique_id = data["id"],
                defaults={
                    "user_info" : data
                }
            )
            if account_obj:
                account_obj.last_updated = timezone.now()
                account_obj.save()
        api_obj = APIReport.objects.create(
            api_url = url,
            date = timezone.now().date()
        )
        return "done"
    except Exception as e:
        traceback.print_exc()
        return "error"