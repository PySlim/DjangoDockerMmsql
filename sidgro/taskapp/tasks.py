from celery.decorators import periodic_task
from celery.schedules import crontab


from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES
from ldap3.core.exceptions import LDAPCursorError

from sidgro.users.models.user import User

from sidgro._event.repository.actionPlan_repository import RepositoryActionPlan
from sidgro._event.repository.actionPlanStatus_repository import ActionPlanStatusRepository

from datetime import date, datetime

#@periodic_task(run_every=(crontab(hour=4)), name="update_directory_active")
@periodic_task(run_every=(crontab(minute='*/10')), name="update_directory_active")
def update_directory_active():
        server = Server('192.168.100.107:389', get_info=ALL)
        conn = Connection(server, user="proempresaqa.com.pe\\admcalidad",password="C4l1d4d2021", authentication=NTLM,auto_bind=True)
        conn.search('dc=proempresaqa,dc=com,dc=pe', '(objectclass=person)',attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
        for e in sorted(conn.entries):
            try:
                desc= e.sAMAccountName
            except LDAPCursorError:
                desc = None
            try:
                user= User.objects.get(nickname=str(desc),name=str(e.name))
            except User.DoesNotExist:
                pass
            else:
                user.userUpdate=True
                user.save()
        user_delete= User.objects.filter(userUpdate=False)
        for user_i in user_delete:
            user_i.delete()
        users = User.objects.all()
        for user in users:
            user.userUpdate=False
            user.save()

@periodic_task(run_every=(crontab(minute=1, hour=0)), name="update_actionPlan_status")
def update_actionPlan_status():
    status_close = ActionPlanStatusRepository().get_actionPlanStatus_by_id(3)
    status_active = ActionPlanStatusRepository().get_actionPlanStatus_by_id(2)
    actionPlans = RepositoryActionPlan().get_actionPlan_active(status_close)
    date_now = date.today()
    for item in actionPlans:
        date_start = item.estimatedDateStart
        date_end = item.estimatedDateEnd
        if date_now == date_start.date():
            item.status = status_active
            item.save()
        if date_now > date_end.date():
            item.status = status_close
            item.save()

        
        


