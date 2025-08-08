from django.db import models


class TTransact(models.Model):
    date = models.TextField()
    time = models.TextField()
    user = models.TextField()
    machine = models.TextField()
    act = models.TextField()
    cash = models.TextField(blank=True, null=True)
    check_amt = models.TextField(blank=True, null=True)
    check_num = models.TextField(blank=True, null=True)
    change = models.TextField(blank=True, null=True)
    cc = models.TextField(blank=True, null=True)
    cc_fee = models.TextField(blank=True, null=True)
    paid_by = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_transact'


class TAccounts(models.Model):
    l_agency = models.TextField(blank=True, null=True)
    s_agency = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_accounts'


class TTransactDetail(models.Model):
    t_transact_id = models.IntegerField()
    t_accounts_id = models.IntegerField()
    t_items_id = models.IntegerField()
    quan = models.TextField(blank=True, null=True)
    ea = models.TextField(blank=True, null=True)
    ex = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_transact_detail'