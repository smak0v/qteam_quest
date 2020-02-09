from django.shortcuts import render, redirect

from apps.games.models import Game
from apps.timeline.forms import TimelineBlockForm
from apps.timeline.models import TimelineBlock
from apps.timeline.utils import create_timeline_block
from users.models import User


def timeline_blocks_list_view(request):
    """Function that implements created by admins timeline blocks list view"""

    admin_timeline_blocks = TimelineBlock.objects.filter(creator='ADMIN').order_by('-timespan')
    app_timeline_blocks = TimelineBlock.objects.filter(creator='APP').order_by('-timespan')
    context = {
        'title': 'Элементы ленты',
        'admin_timeline_blocks': admin_timeline_blocks if admin_timeline_blocks.count() > 0 else None,
        'app_timeline_blocks': app_timeline_blocks if app_timeline_blocks.count() > 0 else None,
    }
    return render(request=request, template_name='timeline/list.html', context=context)


def create_timeline_block_view(request):
    """Function that implements timeline block create view"""

    if request.method == 'POST':
        form = TimelineBlockForm(request.POST, request.FILES)
        if form.is_valid():
            user = None if form.data.get('user') == '' else User.objects.get(pk=form.data.get('user'))
            game = None if form.data.get('game') == '' else Game.objects.get(pk=form.data.get('game'))
            timeline_block_type = form.data.get('type')
            message = form.data.get('message')
            image = request.FILES.get('image', None)
            if user is not None:
                create_timeline_block(timeline_block_type, message, user, 'ADMIN', game, image)
            else:
                users = User.objects.all()
                for _ in users:
                    create_timeline_block(timeline_block_type, message, _, 'ADMIN', game, image)
            return redirect(to='timeline:list')
        else:
            context = {
                'title': 'Создание элемента ленты',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='timeline/create.html', context=context)
    else:
        form = TimelineBlockForm()
        context = {
            'form': form,
            'title': 'Создание элемента ленты',
        }
        return render(request=request, template_name='timeline/create.html', context=context)


def edit_timeline_block_view(request, pk):
    """Function that implements timeline block edit view"""

    timeline_block = TimelineBlock.objects.get(pk=pk)
    if request.method == 'POST':
        form = TimelineBlockForm(request.POST, request.FILES, instance=timeline_block)
        if form.is_valid():
            form.save()
            return redirect(to='timeline:list')
        else:
            context = {
                'title': 'Редактирование элемента ленты',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='timeline/edit.html', context=context)
    else:
        form = TimelineBlockForm(instance=timeline_block)
        context = {
            'title': 'Редактирование элемента ленты',
            'form': form,
        }
        return render(request=request, template_name='timeline/edit.html', context=context)


def delete_timeline_block_view(request, pk):
    """Function that implements timeline block delete view"""

    timeline_block = TimelineBlock.objects.get(pk=pk)
    timeline_block.delete()
    return redirect(to='timeline:list')
