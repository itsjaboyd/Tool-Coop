from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class ToolType(models.Model):
    type_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default='default.jpeg', upload_to='tool_pics')

    def __str__(self):
        return f'{self.type_name} Profile'


class Tool(models.Model):
    tool_type = models.ForeignKey(ToolType, on_delete=models.CASCADE)
    is_available = models.BooleanField (default=True)

    def __str__(self):
        return f'{self.tool_type.type_name} Tool'

class ReservationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    checkout_date = models.DateField()
    checkin_date = models.DateField()
    due_date = models.DateField()
    has_picked_up = models.BooleanField (default=False)

    def __str__(self):
        return f'{self.user.username} ReservationLog'

class ReservationLogTools(models.Model):
    reservation =  models.ForeignKey(ReservationLog, on_delete=models.CASCADE)
    tool = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tool.tool_type.type_name} Reservation log tools'



