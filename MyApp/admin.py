from django.contrib import admin
from .models import Application, Represantative, CommitteeMember, TeamOfficial


admin.site.register(CommitteeMember)
admin.site.register(Represantative)
admin.site.register(Application)
admin.site.register(TeamOfficial)





