from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account, APIReport
from accounts.tasks import bytes_to_json, create_update_user
import requests
import  traceback
from django.utils import timezone
from datetime import timedelta
# Create your views here.

class SearchUser(APIView):
    """
    GET : This method will be used to fetch users from Github search api
    """
    def get(self, request):
        try:
            user_name = request.GET["user_name"]
            followers = request.GET.get("followers")
            repo = request.GET.get("repos")
            page = request.GET.get("page")
            if not page:
                page=1
            else:
                if not page.isdigit():
                    page = 1
                else:
                    pass
            if not str(followers).isdigit():
                followers = None
            if not str(repo).isdigit():
                repo = None
            url = "https://api.github.com/search/users?q="+user_name

            if followers:
                url += "+followers:%3E"+followers
            if repo:
                url += "+repos:%3E"+repo
            url += "&page="+str(page)
            req_search = requests.get(url=url)
            result = bytes_to_json(req_search.content)
            create_update_user.delay(user_data=result["items"], url=url)
            return Response({"success" : True, "data" : result}, status=200)
        except Exception as e:
            traceback.print_exc()
            return Response({"error" : str(e), "success" : False}, status=400)


def report_html(request):
    """
    This method will return stats of how many users was added in a day, week and month and how many a times a api was hit
    :param request: None
    :return: Today (User count, Api hit's today), Week(User and API count in weeek from 7 days before to today),
            Month(User and API count 30 days before to today)
    """

    account_filter = Account.objects.all()
    api_filter = APIReport.objects.all()
    today_date = timezone.now().date()
    #USER STATS
    today_user = account_filter.filter(date_added__date=today_date)
    week_user = account_filter.filter(date_added__date__range=[today_date-timedelta(days=7), today_date])
    month_user = account_filter.filter(date_added__date__range=[today_date-timedelta(days=30), today_date])

    #API STATS
    today_hits = api_filter.filter(date=today_date)
    week_hits = api_filter.filter(date__range=[today_date-timedelta(days=7), today_date])
    month_hits = api_filter.filter(date__range=[today_date-timedelta(days=30), today_date])
    return render(request, "accounts/report.html", context={
        "user_today" : today_user.count(),
        "user_week" : week_user.count(),
        "user_month" : month_user.count(),
        "api_today" : today_hits.count(),
        "api_week" : week_hits.count(),
        "api_month" : month_hits.count()
    })