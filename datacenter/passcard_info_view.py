from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
  passcard = get_object_or_404(Passcard, passcode=passcode)
  visits = Visit.objects.filter(passcard=passcard)

  this_passcard_visits = []
  for vi in visits:
    if vi.leaved_at:
      this_passcard_visits.append({
          'entered_at': vi.entered_at,
          'duration': vi.get_duration(),
          'is_strange': vi.is_long(minutes=1000)
      })

  context = {
      'passcard': passcard,
      'this_passcard_visits': this_passcard_visits
  }
  return render(request, 'passcard_info.html', context)
