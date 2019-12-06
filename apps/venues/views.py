from django.shortcuts import render, redirect
from django.views import View

from apps.games.models import Game
from apps.venues.forms import VenueForm, VenueMetroStationForm
from apps.venues.models import Venue, MetroStation


class VenuesListView(View):
    """Class that represents venues list view"""

    template_name = 'venues/list.html'

    def get(self, request):
        venues = Venue.objects.all().order_by('name')
        context = {
            'venues': venues,
            'title': 'Площадки',
        }
        return render(request=request, template_name=self.template_name, context=context)


def venue_details_view(request, pk):
    """Function that implements venues details view"""

    venue = Venue.objects.get(pk=pk)
    games = Game.objects.filter(venue=venue, cancel=False).order_by('timespan')
    canceled_games = Game.objects.filter(venue=venue, cancel=True).order_by('timespan')
    context = {
        'title': 'Информация по площадке',
        'venue': venue,
        'metro_stations': venue.metro_stations.all(),
        'games': games,
        'canceled_games': canceled_games,
    }
    return render(request=request, template_name='venues/details.html', context=context)


def create_venue_view(request):
    """Function that implements venues create view"""

    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save()
            return redirect(to='venues:list')
        else:
            context = {
                'title': 'Создание площадки',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='venues/create.html', context=context)
    else:
        form = VenueForm()
        context = {
            'title': 'Создание площадки',
            'form': form,
        }
        return render(request=request, template_name='venues/create.html', context=context)


def edit_venue_view(request, pk):
    """Function that implements venues edit view"""

    venue = Venue.objects.get(pk=pk)
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            return redirect(to='venues:list')
        else:
            context = {
                'title': 'Редактирование площадки',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='venues/edit.html', context=context)
    else:
        form = VenueForm(instance=venue)
        context = {
            'title': 'Редактирование площадки',
            'form': form,
        }
        return render(request=request, template_name='venues/edit.html', context=context)


def delete_venue_view(request, pk):
    """Function that implements venues delete view"""

    venue = Venue.objects.get(pk=pk)
    venue.delete()
    return redirect(to='venues:list')


def create_venue_metro_station_view(request, venue_pk):
    """Function that implements venue metro station create view"""

    if request.method == 'POST':
        form = VenueMetroStationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.venue_id = venue_pk
            station.save()
            return redirect(to='venues:details', pk=venue_pk)
        else:
            context = {
                'title': 'Создание станции метро',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='venues/metro_stations/create.html', context=context)
    else:
        form = VenueMetroStationForm()
        context = {
            'title': 'Создание станции метро',
            'form': form,
        }
        return render(request=request, template_name='venues/metro_stations/create.html', context=context)


def edit_venue_metro_station_view(request, venue_pk, station_pk):
    """Function that implements venue metro station edit view"""

    station = MetroStation.objects.get(pk=station_pk)
    if request.method == 'POST':
        form = VenueMetroStationForm(request.POST, instance=station)
        if form.is_valid():
            station = form.save(commit=False)
            station.venue_id = venue_pk
            station.save()
            return redirect(to='venues:details', pk=venue_pk)
        else:
            context = {
                'title': 'Редактирование станции метро',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='venues/metro_stations/edit.html', context=context)
    else:
        form = VenueMetroStationForm(instance=station)
        context = {
            'title': 'Редактирование станции метро',
            'form': form,
        }
        return render(request=request, template_name='venues/metro_stations/edit.html', context=context)


def delete_venue_metro_station_view(request, venue_pk, station_pk):
    """Function that implements venue metro station delete view"""

    MetroStation.objects.get(pk=station_pk).delete()
    return redirect(to='venues:details', pk=venue_pk)
