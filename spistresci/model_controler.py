from django.db.models.fields.related import OneToOneField
from models import MiniBook, MasterBook


def add_MiniBook(bookstore, d):

    pods = {}
    rel = {}
    extras = {}

    columns = MiniBook._meta.get_all_field_names()
    for key, value in d.iteritems():
        if key in columns:
            field, model, direct, m2m = MiniBook._meta.get_field_by_name(key)
            if field.rel:
                rel[key] = (value, field.rel.to)
            else:
                pods[key] = value
        else:
            extras[key] = value

    try:

        book = MiniBook.objects.get(
            external_id=pods['external_id'],
            bookstore=bookstore
        )

        #update

        modified = False
        for key, value in pods.iteritems():
            if unicode(getattr(book, key)) != value:
                modified = True
                setattr(book, key, value)

        if book.extra != extras:
            modified = True
            book.extra = extras

        for key, value in rel.iteritems():
            __rel_class__ = value[1]

            if isinstance(value[0], list):

                rel_objects = []
                for rel_dict in value[0]:

                    rel_obj, created = \
                        __rel_class__.objects.get_or_create(**rel_dict)

                    rel_objects.append(rel_obj)

                attr = getattr(book, key)

                different_length = len(attr.all()) != len(rel_objects)
                not_all_in = not all(
                    rel_obj in attr.all()
                    for rel_obj in rel_objects
                )

                if different_length or not_all_in:
                    modified = True
                    attr.clear()
                    for rel_obj in rel_objects:
                        attr.add(rel_obj)

            else:

                if getattr(book, key) != value[0]:
                    modified = True
                    obj = __rel_class__(**value[0])
                    obj.save()
                    setattr(book, key, obj)

        if modified:
            book.save()

    except MiniBook.DoesNotExist:

        pods['bookstore'] = bookstore
        pods['extra'] = extras

        book = MiniBook(**pods)
        book.save()

        for key, value in rel.iteritems():
            __rel_class__ = value[1]

            if isinstance(value[0], list):
                for rel_dict in value[0]:

                    rel_obj, created = \
                        __rel_class__.objects.get_or_create(**rel_dict)

                    getattr(book, key).add(rel_obj)

            elif isinstance(
                    MiniBook._meta.get_field_by_name(key)[0],
                    OneToOneField
            ):
                obj = __rel_class__.objects.create(**value[0])
                setattr(book, key, obj)

            else:
                obj, created = __rel_class__.objects.get_or_create(**value[0])
                setattr(book, key, obj)

        book.save()

        master = MasterBook(
            title=book.title,
            cover=book.cover
        )
        master.save()

        for format in book.formats.all():
            master.formats.add(format)

        book.master = master
        book.master.save()
        book.save()

        print "test"


    return book