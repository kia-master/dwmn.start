from datacenter.models import Passcard
from datacenter.models import Visit, format_duration
from django.shortcuts import render


def storage_information_view(request):
    not_leaved_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []

    for visit in not_leaved_visits:
      duration = visit.get_duration()
      non_closed_visits.append(
        {
          'who_entered': Passcard.objects.get(pk=visit.passcard_id).owner_name,
          'entered_at': visit.entered_at,
          'duration': format_duration(duration),
        }
      )
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
