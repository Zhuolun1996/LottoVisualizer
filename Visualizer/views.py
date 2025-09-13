from datetime import datetime

from django.shortcuts import render, redirect

from Visualizer.models import LottoDraw, LottoType
import requests
from bs4 import BeautifulSoup


# Create your views here.
def home(request):
    return render(request, "home.html")


def show_drawing(request):
    retrieve_count = request.GET.get("retrieve_count")
    lotto = request.GET.get("lotto")
    if not retrieve_count:
        retrieve_count = 10
    else:
        retrieve_count = int(retrieve_count)
    if not lotto:
        lotto = "PowerBall"
    drawings = LottoDraw.objects.filter(lotto_type__name=lotto).order_by("-lotto_date")[:retrieve_count][::-1]
    lotto_type = LottoType.objects.get(name=lotto)
    context = {
        "drawings": drawings,
        "lotto_type": lotto_type,
        "lotto_range": range(1, lotto_type.nums + 1)
    }
    if lotto_type.has_special:
        context["special_range"] = range(1, lotto_type.special_nums + 1)
    return render(request, "show_drawing.html", context)


def update_data(remote_url, lotto_type):
    response = requests.get(remote_url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_drawings = soup.find_all("table", class_="table-viewport-small")
    for drawing in all_drawings:
        date = datetime.strptime(drawing.find("p", class_="h2-like").text, "%a, %b %d, %Y").date()
        numbers_list = [str(int(x.text)) for x in drawing.find("td", class_="game-balls").find("ul").find_all("li")]
        numbers = ",".join(numbers_list)
        LottoDraw.objects.get_or_create(lotto_number=numbers, lotto_date=date,
                                        lotto_type=LottoType.objects.get(name=lotto_type))


def update_data_powerball(request):
    update_data(
        "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=powerball&unittype=day&unitcount=180",
        "PowerBall")
    return redirect("/show_drawing/?retrieve_count=10&lotto=PowerBall")


def update_data_wa_lotto(request):
    update_data(
        "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=lotto&unittype=day&unitcount=180",
        "WALotto")
    return redirect("/show_drawing/?retrieve_count=10&lotto=WALotto")

def update_data_hit5(request):
    update_data(
        "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=hit5&unittype=day&unitcount=180",
        "Hit5")
    return redirect("/show_drawing/?retrieve_count=10&lotto=Hit5")


def update_data_match4(request):
    update_data(
        "https://www.walottery.com/WinningNumbers/PastDrawings.aspx?gamename=match4&unittype=day&unitcount=180",
        "Match4")
    return redirect("/show_drawing/?retrieve_count=10&lotto=Match4")

