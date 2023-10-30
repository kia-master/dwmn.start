from django.db import models
import datetime
from django.utils.timezone import localtime, now


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self, leaved=False) -> datetime.timedelta:
      if leaved:
        time_difference = localtime(self.leaved_at) - localtime(self.entered_at)
      else:
        time_difference = now() - localtime(self.entered_at)
      return datetime.timedelta(days=time_difference.days,
                                seconds=time_difference.seconds)

    def is_long(self, minutes=10) -> bool | None:
      visit_finish_time = self.get_duration(leaved=True)
      return visit_finish_time.total_seconds() > minutes * 60

  
def format_duration(duration: datetime.timedelta):
  days, seconds = duration.days, duration.seconds
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  if days == 0:
      return f'{hours}ч {minutes}мин'
  return f'{days}д {hours}ч {minutes}мин'
