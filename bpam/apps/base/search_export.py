from django.db.models.fields.related import ForeignKey
from apps.common.models import BPAUniqueID


class CSVExporter(object):

    def __init__(self, model):
        self.model = model
        self.one_object_per_id = True

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
        export_file_obj.flush()
        export_file_obj.seek(0)
        return export_file_obj


    def _get_csv_filename(self):
        return "%s.csv" % self.model.__name__

    def _get_headers(self):
        return [pair[1] for pair in self.field_data]

    def _get_rows(self, ids):
        for id in ids:
            if self.one_object_per_id:
                model_instance = self._get_instance(id)
                instances = [ model_instance]
            else:
                instances = self._get_instance(id)

            for instance in instances:
                values = []
                for field_pair in self.field_data:

                    field_path = field_pair[0]
                    parts = field_path.split(".")
                    try:
                        value = reduce(getattr, parts, instance)
                    except AttributeError:
                        value = "None"

                    values.append(value)
                yield values

    def _get_instance(self, id):
        try:
            bpa_id = BPAUniqueID.objects.get(bpa_id=id)
        except BPAUniqueID.DoesNotExist:
            return None

        return self._get_model_for_id(bpa_id)

    def _get_model_for_id(self, bpa_id):
            if self.one_object_per_id:
                try:
                    return self.model.objects.get(bpa_id=bpa_id)

                except self.model.DoesNotExist:
                    return None
            else:
                return self.model.objects.filter(bpa_id=bpa_id)


class OTUExporter(CSVExporter):
    def __init__(self, kingdom, phylum, otu_class, order, family, genus, species):
        from apps.base_otu.models import SampleOTU
        super(OTUExporter, self).__init__(SampleOTU)
        self.one_object_per_id = False
        self.kingdom = kingdom
        self.phylum = phylum
        self.otu_class = otu_class
        self.order = order
        self.family = family
        self.genus = genus
        self.species = species
        self.taxonomic_filters = {}

        def add_taxonomic_filter(filter_dict, taxon):
            value = getattr(self, taxon)
            if value != '---':
                filter_dict["otu__" + taxon] = getattr(self, taxon)

        for taxon in ['kingdom', 'phylum', 'otu_class', 'order', 'family', 'genus', 'species']:
            add_taxonomic_filter(self.taxonomic_filters, taxon)

    def _get_model_for_id(self, bpa_id):
        filter_dict = {"sample__bpa_id__bpa_id": bpa_id.bpa_id}
        filter_dict.update(self.taxonomic_filters)
        return self.model.objects.filter(**filter_dict)

    def _get_fields(self, model, prefix=""):
        return [["sample.bpa_id.bpa_id", "BPA ID"],
                ["otu.name", "OTU"],
                ["count", "OTU Count"],
                ["otu.kingdom", "Kingdom"],
                ["otu.phylum", "Phylum"],
                ["otu.otu_class", "Class"],
                ["otu.order", "Order"],
                ["otu.family", "Family"],
                ["otu.genus", "Genus"],
                ["otu.species", "Species"],
                ]

    def export(self, ids, file_obj_16S, file_obj_18S, file_obj_ITS):

        import csv
        writer16S = csv.writer(file_obj_16S)
        writer18S = csv.writer(file_obj_18S)
        writerITS = csv.writer(file_obj_ITS)

        self.field_data = self._get_fields(self.model)

        writer16S.writerow(self._get_headers())
        writer18S.writerow(self._get_headers())
        writerITS.writerow(self._get_headers())
        for row in self._get_rows(ids):
            kingdom = row[3]
            if kingdom == "Bacteria":
                writer16S.writerow(row)
            elif kingdom == "Fungi":
                writerITS.writerow(row)
            elif kingdom == "Eukaryote":
                writer18S.writerow(row)
            else:
                # Archaea??!
                pass

        file_obj_16S.flush()
        file_obj_16S.seek(0)

        file_obj_18S.flush()
        file_obj_18S.seek(0)

        file_obj_ITS.flush()
        file_obj_ITS.seek(0)

        return file_obj_16S, file_obj_18S, file_obj_ITS