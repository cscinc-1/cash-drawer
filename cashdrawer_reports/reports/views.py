from django.shortcuts import render
from django.db.models import Sum, Count
from django.db import connection
from decimal import Decimal
from .models import TTransact, TAccounts, TTransactDetail
from datetime import datetime


def daily_transactions(request):
    # Get date from query params or use default
    date_str = request.GET.get('date', '2018-02-13')
    
    # Query transactions for the specified date
    transactions = TTransact.objects.filter(date=date_str, act='pay').order_by('machine', 'id')
    
    # Group transactions by drawer/machine
    drawers = {}
    for transaction in transactions:
        machine = transaction.machine
        if machine not in drawers:
            drawers[machine] = {
                'transactions': [],
                'cash_total': Decimal('0.00'),
                'check_total': Decimal('0.00'),
                'card_total': Decimal('0.00'),
                'change_total': Decimal('0.00')
            }
        
        # Convert text fields to Decimal for calculations
        cash = Decimal(transaction.cash) if transaction.cash else Decimal('0.00')
        check_amt = Decimal(transaction.check_amt) if transaction.check_amt else Decimal('0.00')
        card = Decimal(transaction.cc) if transaction.cc else Decimal('0.00')
        change = Decimal(transaction.change) if transaction.change else Decimal('0.00')
        
        drawers[machine]['transactions'].append({
            'id': transaction.id,
            'user': transaction.user,
            'cash': cash,
            'check_amt': check_amt,
            'card': card,
            'change': change,
            'check_num': transaction.check_num or '',
            'paid_by': transaction.paid_by or ''
        })
        
        drawers[machine]['cash_total'] += cash
        drawers[machine]['check_total'] += check_amt
        drawers[machine]['card_total'] += card
        drawers[machine]['change_total'] += change
    
    # Calculate day totals
    day_totals = {
        'cash': sum(d['cash_total'] for d in drawers.values()),
        'check': sum(d['check_total'] for d in drawers.values()),
        'card': sum(d['card_total'] for d in drawers.values()),
        'change': sum(d['change_total'] for d in drawers.values())
    }
    
    # Calculate report total (Cash + Check + Card - Change)
    report_total = day_totals['cash'] + day_totals['check'] + day_totals['card'] - day_totals['change']
    
    # Sort drawers by name
    sorted_drawers = dict(sorted(drawers.items()))
    
    context = {
        'date': date_str,
        'drawers': sorted_drawers,
        'day_totals': day_totals,
        'report_total': report_total
    }
    
    return render(request, 'reports/daily_transactions.html', context)


def accounts_report(request):
    # Get date from query params or use default
    date_str = request.GET.get('date', '2018-02-13')
    
    # Raw SQL query to get account-based transactions
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                ta.id as account_id,
                ta.l_agency,
                ta.s_agency,
                COUNT(DISTINCT t.id) as transaction_count,
                SUM(CASE WHEN t.cash IS NOT NULL AND t.cash != '' THEN CAST(t.cash AS REAL) ELSE 0 END) as cash_total,
                SUM(CASE WHEN t.check_amt IS NOT NULL AND t.check_amt != '' THEN CAST(t.check_amt AS REAL) ELSE 0 END) as check_total,
                SUM(CASE WHEN t.cc IS NOT NULL AND t.cc != '' THEN CAST(t.cc AS REAL) ELSE 0 END) as card_total,
                SUM(CASE WHEN t.change IS NOT NULL AND t.change != '' THEN CAST(t.change AS REAL) ELSE 0 END) as change_total,
                SUM(CASE WHEN td.ex IS NOT NULL AND td.ex != '' THEN CAST(td.ex AS REAL) ELSE 0 END) as item_total
            FROM t_transact t
            LEFT JOIN t_transact_detail td ON t.id = td.t_transact_id
            LEFT JOIN t_accounts ta ON td.t_accounts_id = ta.id
            WHERE t.date = %s 
                AND t.act = 'pay'
                AND ta.l_agency IS NOT NULL
            GROUP BY ta.id, ta.l_agency, ta.s_agency
            ORDER BY ta.l_agency
        """, [date_str])
        
        columns = [col[0] for col in cursor.description]
        accounts_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Get individual transactions for each account
    accounts = {}
    for account in accounts_data:
        account_id = account['account_id']
        l_agency = account['l_agency']
        
        # Get transactions for this account
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT
                    t.id,
                    t.user,
                    t.machine,
                    t.time,
                    t.cash,
                    t.check_amt,
                    t.check_num,
                    t.cc as card,
                    t.change,
                    t.paid_by,
                    td.ex as item_amount
                FROM t_transact t
                JOIN t_transact_detail td ON t.id = td.t_transact_id
                WHERE td.t_accounts_id = %s
                    AND t.date = %s
                    AND t.act = 'pay'
                ORDER BY t.time
            """, [account_id, date_str])
            
            trans_columns = [col[0] for col in cursor.description]
            transactions = []
            
            for row in cursor.fetchall():
                trans_dict = dict(zip(trans_columns, row))
                # Convert to Decimal for display
                trans_dict['cash'] = Decimal(trans_dict['cash']) if trans_dict['cash'] else Decimal('0.00')
                trans_dict['check_amt'] = Decimal(trans_dict['check_amt']) if trans_dict['check_amt'] else Decimal('0.00')
                trans_dict['card'] = Decimal(trans_dict['card']) if trans_dict['card'] else Decimal('0.00')
                trans_dict['change'] = Decimal(trans_dict['change']) if trans_dict['change'] else Decimal('0.00')
                trans_dict['item_amount'] = Decimal(trans_dict['item_amount']) if trans_dict['item_amount'] else Decimal('0.00')
                transactions.append(trans_dict)
        
        accounts[l_agency] = {
            's_agency': account['s_agency'],
            'transactions': transactions,
            'cash_total': Decimal(str(account['cash_total'] or 0)),
            'check_total': Decimal(str(account['check_total'] or 0)),
            'card_total': Decimal(str(account['card_total'] or 0)),
            'change_total': Decimal(str(account['change_total'] or 0)),
            'item_total': Decimal(str(account['item_total'] or 0)),
            'transaction_count': account['transaction_count']
        }
    
    # Calculate totals
    totals = {
        'cash': sum(a['cash_total'] for a in accounts.values()),
        'check': sum(a['check_total'] for a in accounts.values()),
        'card': sum(a['card_total'] for a in accounts.values()),
        'change': sum(a['change_total'] for a in accounts.values()),
        'items': sum(a['item_total'] for a in accounts.values()),
        'transaction_count': sum(a['transaction_count'] for a in accounts.values())
    }
    
    # Calculate report total
    report_total = totals['cash'] + totals['check'] + totals['card'] - totals['change']
    
    context = {
        'date': date_str,
        'accounts': accounts,
        'totals': totals,
        'report_total': report_total
    }
    
    return render(request, 'reports/accounts_report.html', context)