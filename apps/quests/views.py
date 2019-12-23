from django.shortcuts import render, redirect
from django.views import View

from apps.games.models import Game
from apps.quests.forms import QuestForm, QuestMetroStationForm
from apps.quests.models import Quest, MetroStation


class QuestListView(View):
    """Class that represents games list view"""

    @staticmethod
    def get(request):
        quests = Quest.objects.all().order_by('name')
        context = {
            'quests': quests,
            'title': 'Квесты',
        }
        return render(request=request, template_name='quests/list.html', context=context)


def quest_details_view(request, pk):
    """Function that implements quests details view"""

    quest = Quest.objects.get(pk=pk)
    games = Game.objects.filter(quest=quest, cancel=False).order_by('timespan')
    canceled_games = Game.objects.filter(quest=quest, cancel=True).order_by('timespan')
    context = {
        'title': 'Информация по квесту',
        'quest': quest,
        'metro_stations': quest.metro_stations.all(),
        'games': games,
        'canceled_games': canceled_games,
    }
    return render(request=request, template_name='quests/details.html', context=context)


def create_quest_view(request):
    """Function that implements quests create view"""

    if request.method == 'POST':
        form = QuestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(to='quests:list')
        else:
            context = {
                'title': 'Создание квеста',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='quests/create.html', context=context)
    else:
        form = QuestForm()
        context = {
            'title': 'Создание квеста',
            'form': form,
        }
        return render(request=request, template_name='quests/create.html', context=context)


def edit_quest_view(request, pk):
    """Function that implements quests edit view"""

    quest = Quest.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestForm(request.POST, request.FILES, instance=quest)
        if form.is_valid():
            form.save()
            return redirect(to='quests:list')
        else:
            context = {
                'title': 'Редактирование квеста',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='quests/edit.html', context=context)
    else:
        form = QuestForm(instance=quest)
        context = {
            'title': 'Редактирование квеста',
            'form': form,
        }
        return render(request=request, template_name='quests/edit.html', context=context)


def delete_quest_view(request, pk):
    """Function that implements quests delete view"""

    quest = Quest.objects.get(pk=pk)
    quest.delete()
    return redirect(to='quests:list')


def create_quest_metro_station_view(request, quest_pk):
    """Function that implements quests metro station create view"""

    if request.method == 'POST':
        form = QuestMetroStationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.quest_id = quest_pk
            station.save()
            return redirect(to='quests:details', pk=quest_pk)
        else:
            context = {
                'title': 'Создание станции метро',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='quests/metro_stations/create.html', context=context)
    else:
        form = QuestMetroStationForm()
        context = {
            'title': 'Создание станции метро',
            'form': form,
        }
        return render(request=request, template_name='quests/metro_stations/create.html', context=context)


def edit_quest_metro_station_view(request, quest_pk, station_pk):
    """Function that implements quests metro station edit view"""

    station = MetroStation.objects.get(pk=station_pk)
    if request.method == 'POST':
        form = QuestMetroStationForm(request.POST, instance=station)
        if form.is_valid():
            station = form.save(commit=False)
            station.quest_id = quest_pk
            station.save()
            return redirect(to='quests:details', pk=quest_pk)
        else:
            context = {
                'title': 'Редактирование станции метро',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='quests/metro_stations/edit.html', context=context)
    else:
        form = QuestMetroStationForm(instance=station)
        context = {
            'title': 'Редактирование станции метро',
            'form': form,
        }
        return render(request=request, template_name='quests/metro_stations/edit.html', context=context)


def delete_quest_metro_station_view(request, quest_pk, station_pk):
    """Function that implements venue metro station delete view"""

    MetroStation.objects.get(pk=station_pk).delete()
    return redirect(to='quests:details', pk=quest_pk)
