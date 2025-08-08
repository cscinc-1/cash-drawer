# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SqliteSpFunctions(models.Model):
    name = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sqlite_sp_functions'


class SqliteStat1(models.Model):
    tbl = models.TextField(blank=True, null=True)  # This field type is a guess.
    idx = models.TextField(blank=True, null=True)  # This field type is a guess.
    stat = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sqlite_stat1'


class SqliteVsDiagrams(models.Model):
    name = models.TextField(blank=True, null=True)
    diadata = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    preview = models.BinaryField(blank=True, null=True)
    preview_full = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sqlite_vs_diagrams'


class SqliteVsLinks(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sqlite_vs_links'


class SqliteVsLinksNames(models.Model):
    name = models.TextField(blank=True, null=True)
    alias = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sqlite_vs_links_names'


class SqliteVsProperties(models.Model):
    parenttype = models.TextField(db_column='parentType', blank=True, null=True)  # Field name made lowercase.
    parentname = models.TextField(db_column='parentName', blank=True, null=True)  # Field name made lowercase.
    propertyname = models.TextField(db_column='propertyName', blank=True, null=True)  # Field name made lowercase.
    propertyvalue = models.TextField(db_column='propertyValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sqlite_vs_properties'


class TAccounts(models.Model):
    l_agency = models.TextField(blank=True, null=True)
    s_agency = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_accounts'


class TCcFees(models.Model):
    id = models.IntegerField(blank=True, null=True)
    bottom = models.FloatField(blank=True, null=True)
    top = models.FloatField(blank=True, null=True)
    fee = models.TextField(blank=True, null=True)
    pct = models.TextField(blank=True, null=True)
    both = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_cc_fees'


class TData(models.Model):
    key = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_data'


class TItems(models.Model):
    sname = models.TextField(blank=True, null=True)
    lname = models.TextField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_items'


class TItemsDetail(models.Model):
    t_items_id = models.IntegerField()
    t_accounts_id = models.IntegerField()
    amount = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_items_detail'


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


class TUsers(models.Model):
    user = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_users'
