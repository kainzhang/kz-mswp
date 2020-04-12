from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from record.models import Record


# Create your views here.

class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = '__all__'

    def clean(self):
        if self.cleaned_data['difficulty'] < 1 and self.cleaned_data['difficulty'] > 4:
            raise forms.ValidationError('Invalid difficulty')

        if self.cleaned_data['finish_time'] <= 0:
            raise forms.ValidationError('Invalid finish time')

        player_id = self.cleaned_data['player']
        player = auth.authenticate(pk=player_id)
        if player is None:
            raise forms.ValidationError('Invalid User')

        return self.cleaned_data


def record_list(request):
    data = {}
    difficulty = int(request.GET.get('difficulty', default=1))
    objs = Record.objects.filter(difficulty=difficulty).order_by('finish_time')
    data['object_list'] = objs
    if difficulty == 1:
        data['difficulty'] = 'Beginner'
    elif difficulty == 2:
        data['difficulty'] = 'Intermediate'
    elif difficulty == 3:
        data['difficulty'] = 'Expert'

    return render(request, 'record_list.html', data)


def user_record(request):
    data = {}
    player_id = request.GET.get('player_id')
    player = get_object_or_404(User, pk=player_id)

    if player is not None:
        objs = Record.objects.filter(player_id=player_id)
        data['object_list'] = objs.order_by('difficulty')
        data['player_name'] = player.username
        return render(request, 'user_record.html', data)
    else:
        return redirect('index')


def record_insert(request):
    form = RecordForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect(request.GET.get('form', reverse('index')))
