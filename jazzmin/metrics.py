# managers/base_metrics_manager.py
import logging 
from django.db.models import Sum, Avg, Min, Max
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta   

logger = logging.getLogger(__name__)

class MetricsManager():

    def convert_date_str(self, date_str):
        if date_str.lower() == "today":
            return datetime.now()
        if date_str.lower() == "1st of year":
            return datetime(datetime.today().year, 1, 1)

        val = int(date_str[:-1].replace("-",""))
        has_minus = False if "-" not in date_str else True
        if "M" in date_str:
            if has_minus:
                return datetime.now() - relativedelta(months=val)
            return datetime.now() + relativedelta(months=val)
        elif "D" in date_str:
            if has_minus:
                return datetime.now() - relativedelta(days=val)
            return datetime.now() + relativedelta(days=val)
        elif "Y" in date_str:
            if has_minus:
                return datetime.now() - relativedelta(years=val)
            return datetime.now() + relativedelta(years=val)    
        elif "W" in date_str:
            if has_minus:
                return datetime.now() - relativedelta(weeks=val)
            return datetime.now() + relativedelta(weeks=val)   
        elif "h" in date_str:
            if has_minus:
                return datetime.now() - relativedelta(hours=val)
            return datetime.now() + relativedelta(hours=val)   
        elif "m" in date_str:
            if has_minus:
                return datetime.now() - relativedelta(minutes=val)
            return datetime.now() + relativedelta(minutes=val)   
        elif "s" in date_str:
            if has_minus:
                return datetime.now() - relativedelta(seconds=val)
            return datetime.now() + relativedelta(seconds=val)   

    def sum(self, model, column=None, start_date=None, end_date=None, method=None):
        """Calculate the total sum of a field within a date range."""
        if start_date and end_date:
            queryset = model.objects.filter(created__range=(self.convert_date_str(start_date), self.convert_date_str(end_date)))
        else:
            queryset = model.objects.all()
        if method:
            vals = []
            for x in queryset:
                val_method = getattr(x, method)
                vals.append(val_method())
            return f'{round(sum(vals), 2):,}'
            
        return f'{round(queryset.aggregate(val=Sum(column))['val'] or 0, 2):,}'

    def average(self, model, column=None, start_date=None, end_date=None, method=None):
        """Calculate the average of a field within a date range."""
        if start_date and end_date:
            queryset = model.objects.filter(created__range=(self.convert_date_str(start_date), self.convert_date_str(end_date)))
        else:
            queryset = model.objects.all()
        if len(queryset) == 0:
            return f'0'
        if method:
            vals = []
            for x in queryset:
                val_method = getattr(x, method)
                vals.append(val_method())
            return f'{round(sum(vals) / len(vals), 2):,}'
        return f'{round(queryset.aggregate(val=Avg(column))['val'] or 0, 2):,}'

    def max_value(self, model, column=None, start_date=None, end_date=None, method=None):
        """Find the maximum value of a field within a date range."""
        if start_date and end_date:
            queryset = model.objects.filter(created__range=(self.convert_date_str(start_date), self.convert_date_str(end_date)))
        else:
            queryset = model.objects.all()
        return f'{round(queryset.aggregate(val=Max(column))['val'] or 0, 2):,}'

    def min_value(self, model, column=None, start_date=None, end_date=None, method=None):
        """Find the minimum value of a field within a date range."""
        if start_date and end_date:
            queryset = model.objects.filter(created__range=(self.convert_date_str(start_date), self.convert_date_str(end_date)))
        else:
            queryset = model.objects.all()
        return f'{round(queryset.aggregate(val=Min(column))['val'] or 0, 2):,}'

    def count(self, model,column=None, column_val=None, start_date=None, end_date=None, method=None):
        """Count the number of records within a date range."""
        if start_date and end_date:
            queryset = model.objects.filter(created__range=(self.convert_date_str(start_date), self.convert_date_str(end_date)))
        else:
            queryset = model.objects.all()
        return f'{round(queryset.count(), 2):,}'

