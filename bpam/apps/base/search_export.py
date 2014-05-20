from django.db.models.fields.related import ForeignKey
from apps.common.models import BPAUniqueID


class CSVExporter(object):

    def __init__(self, model):
        self.model = model

    def _get_fields(self, model, prefix=""):
        fields = []
        for field in model._meta.fields:
            if field.name == 'debug_note':
                continue
            if model.__name__ == 'LandUse' and field.name == 'parent':
                # this was casuing infinite loop ...
                continue

            verbose_name = "%s" % field.name
            if not verbose_name:
                verbose_name = field.name

            if prefix:
                    name = prefix + "." + field.name
            else:
                    name = field.name

            if not isinstance(field, ForeignKey):

                fields.append([name, name])
            else:
                related_model = field.rel.to
                fields.extend(self._get_fields(related_model, name))
        return fields

    def export(self, ids, export_file_obj):
        import csv
        writer = csv.writer(export_file_obj)
        self.field_data = self._get_fields(self.model)
        writer.writerow(self._get_headers())
        for row in self._get_rows(ids):
            writer.writerow(row)

        return export_file_obj


    def _get_csv_filename(self):
        return "%s.csv" % self.model.__name__

    def _get_headers(self):
        return [pair[1] for pair in self.field_data]

    def _get_rows(self, ids):
        print self.field_data
        for id in ids:
            values = []
            model_instance = self._get_instance(id)
            for field_pair in self.field_data:

                field_path = field_pair[0]
                parts = field_path.split(".")
                try:
                    value = reduce(getattr, parts, model_instance)
                except AttributeError:
                    value = "None"

                values.append(value)
            yield values

    def _get_instance(self, id):
        try:
            bpa_id = BPAUniqueID.objects.get(bpa_id=id)
        except BPAUniqueID.DoesNotExist:
            return None
        try:
            return self.model.objects.get(bpa_id=bpa_id)
        except self.model.DoesNotExist:
            return None