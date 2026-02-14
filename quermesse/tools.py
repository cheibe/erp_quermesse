def update_data():
    from quermesse.models import Caixa, ItemCaixa, Cortesia, ItemCortesia
    from django.db.models import OuterRef, Subquery
    from django.db import transaction

    subCaixa = Caixa.objects.filter(id=OuterRef('caixa_id')).values('created')[:1]
    subCortesia = Cortesia.objects.filter(id=OuterRef('cortesia_id')).values('created')[:1]

    with transaction.atomic():
        ItemCaixa.objects.filter(created__year=2026).update(
            created=Subquery(subCaixa)
        )

        ItemCortesia.objects.filter(created__year=2026).update(
            created=Subquery(subCortesia)
        )

update_data()