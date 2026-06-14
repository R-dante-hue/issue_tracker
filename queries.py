"""
Поисковые запросы для Issue Tracker
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Count, F
from webapp.models import Issue, Status, Type


def closed_last_month():
    """Закрытые задачи за последний месяц (по дате обновления)"""
    one_month_ago = timezone.now() - timedelta(days=30)
    return Issue.objects.filter(
        status__name='Done',
        updated_at__gte=one_month_ago
    )


def specific_status_and_type():
    """Задачи с одним из указанных статусов И одним из указанных типов"""
    return Issue.objects.filter(
        status__name__in=['New', 'In Progress'],
        types__name__in=['Bug', 'Task']
    ).distinct()


def not_closed_bug():
    """Не закрытые задачи, где в названии 'bug' или тип 'Bug'"""
    return Issue.objects.filter(
        Q(summary__icontains='bug') | Q(types__name='Bug')
    ).exclude(status__name='Done').distinct()


def fields_only():
    """Только поля: id, название задачи, тип, статус"""
    return Issue.objects.values('id', 'summary', 'types__name', 'status__name')


def same_summary_description():
    """Задачи, где краткое описание совпадает с полным"""
    return Issue.objects.filter(summary=F('description'))


def count_by_type():
    """Количество задач по каждому типу"""
    return Type.objects.annotate(issue_count=Count('issues')).values('name', 'issue_count')


if __name__ == '__main__':
    print("=== Закрытые задачи за последний месяц ===")
    for issue in closed_last_month():
        print(f"  {issue.summary} ({issue.status.name})")
    if not closed_last_month():
        print("  Нет задач")

    print("\n=== Задачи New/In Progress И Bug/Task ===")
    for issue in specific_status_and_type():
        print(f"  {issue.summary} | {issue.status.name} | {[t.name for t in issue.types.all()]}")
    if not specific_status_and_type():
        print("  Нет задач")

    print("\n=== Не закрытые задачи с bug ===")
    for issue in not_closed_bug():
        print(f"  {issue.summary}")
    if not not_closed_bug():
        print("  Нет задач")

    print("\n=== Только нужные поля ===")
    for item in fields_only():
        print(f"  {item}")

    print("\n=== Где summary == description ===")
    for issue in same_summary_description():
        print(f"  {issue.summary}")
    if not same_summary_description():
        print("  Нет задач")

    print("\n=== Количество задач по типам ===")
    for item in count_by_type():
        print(f"  {item['name']}: {item['issue_count']}")