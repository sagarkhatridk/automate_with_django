from django.shortcuts import render, redirect, get_object_or_404
from dal import autocomplete
from .models import Stock, StockData
from .forms import StockForm
from .utils import scrape_stock_data
from django.contrib import messages

# Create your views here.


class StockAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Stock.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def stocks(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock_id = request.POST["stock"]
            stock = Stock.objects.get(pk=stock_id)
            symbol = stock.symbol
            exchange = stock.exchange
            stock_reponse = scrape_stock_data(symbol, exchange)

            if stock_reponse:
                try:
                    stock_data = StockData.objects.get(stock=stock)
                except StockData.DoesNotExist:
                    stock_data = StockData(stock=stock)

                stock_data.current_price = stock_reponse["current_price"]
                stock_data.price_changed = stock_reponse["price_changed"]
                stock_data.percentage_changed = stock_reponse["percentage_changed"]
                stock_data.previous_close = stock_reponse["previous_close"]
                stock_data.week_52_high = stock_reponse["week_52_high"]
                stock_data.week_52_low = stock_reponse["week_52_low"]
                stock_data.market_cap = stock_reponse["market_cap"]
                stock_data.pe_ratio = stock_reponse["pe_ratio"]
                stock_data.divident_yield = stock_reponse["divident_yield"]
                stock_data.save()
                print("data updated")
                return redirect("stock_detail", stock_data.id)
                # update the stockdata instance with the response data

            else:
                messages.error(request, f"Could not fetch data for {symbol}")
                return redirect("stocks")

    else:
        form = StockForm()
        context = {"form": form}
        return render(request, "stockanalysis/stocks.html", context)


def stock_detail(request, pk):
    stock_data = get_object_or_404(StockData, pk=pk)
    context = {"stock_data": stock_data}
    return render(request, "stockanalysis/stock_detail.html", context)
