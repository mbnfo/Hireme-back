from django.contrib import admin
from base.models import Consumer, Worker, Job, Review, Reciept, Problem, Bids, Notifications
#from .models import Note

admin.site.register(Consumer)
admin.site.register(Worker)
admin.site.register(Job)
admin.site.register(Review)
admin.site.register(Reciept)
admin.site.register(Problem)
admin.site.register(Bids)
admin.site.register(Notifications)