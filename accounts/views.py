from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.tasks import bytes_to_json, create_update_user
import requests
import  traceback
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
            create_update_user.delay(result["items"])
            return Response({"success" : True, "data" : result}, status=200)
        except Exception as e:
            traceback.print_exc()
            return Response({"error" : str(e), "success" : False}, status=400)
