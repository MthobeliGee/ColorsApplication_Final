from django.contrib import admin
from .models import Application, Represantative, CommitteeMember, TeamOfficial, FederationPersonel


admin.site.register(CommitteeMember)
admin.site.register(Represantative)
admin.site.register(Application)
admin.site.register(TeamOfficial)
admin.site.register(FederationPersonel)





