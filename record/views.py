from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from record.models import Record, BestRecord


# Create your views here.

def record_list(request):
    context = {}
    difficulty = int(request.GET.get('difficulty', default=1))
    objs = BestRecord.objects.filter(difficulty=difficulty).order_by('finish_time')
    context['object_list'] = objs

    if difficulty == 1:
        context['difficulty'] = 'Beginner'
    elif difficulty == 2:
        context['difficulty'] = 'Intermediate'
    elif difficulty == 3:
        context['difficulty'] = 'Expert'

    return render(request, 'record_list.html', context)


def user_record(request):
    data = {}
    player_id = request.GET.get('player_id')
    difficulty = request.GET.get('difficulty')
    player = get_object_or_404(User, pk=player_id)

    if player is not None:
        objs = Record.objects.filter(Q(player_id=player_id) & Q(difficulty=difficulty)).order_by('finish_time')
        data['object_list'] = objs.order_by('finish_time')
        data['player'] = player
        return render(request, 'user_record.html', data)
    else:
        return redirect('index')


def record_insert(request):
    player_id = request.POST.get('player_id')
    difficulty = request.POST.get('difficulty')
    finish_time = request.POST.get('finish_time')

    player = User.objects.get(pk=player_id)
    record = Record()
    record.player = player
    record.difficulty = difficulty
    record.finish_time = finish_time
    record.save()

    try:
        best_record = BestRecord.objects.get(player_id=player_id, difficulty=difficulty)
    except BestRecord.DoesNotExist:
        best_record = None

    if best_record is None:
        best_record = BestRecord()
        best_record.player = player
        best_record.difficulty = difficulty
        best_record.finish_time = 999999999999

    best_record.finish_time = min(best_record.finish_time, int(finish_time))
    best_record.save()

    return redirect('index')
