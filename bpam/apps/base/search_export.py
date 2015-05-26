# -*- coding: utf-8 -*-

import logging
import csv

from django.db.models.fields.related import ForeignKey
from apps.common.models import BPAUniqueID


logger = logging.getLogger("rainbow")


class CSVExporter(object):
    def __init__(self, model):
        self.model = model
        self.one_object_per_id = True
        self.field_data = None

    def _get_fields(self, model, prefix=""):
        fields = []
        for field in model._meta.fields:
            if field.name == 'debug_note':
                continue
            if model.__name__ == 'LandUse' and field.name == 'parent':
                continue

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
        for _id in ids:
            if self.one_object_per_id:
                model_instance = self._get_instance(_id)
                if model_instance is None:
                    instances = []
                else:
                    instances = [model_instance]
            else:
                instances = self._get_instance(_id)

            if instances is None:
                instances = []

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

    def _get_instance(self, _id):
        try:
            bpa_id = BPAUniqueID.objects.get(bpa_id=_id)
        except BPAUniqueID.DoesNotExist:
            logger.info("bpa_id %s does not exist!" % _id)
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
        self.field_data = None

        def add_taxonomic_filter(filter_dict, _taxon):
            value = getattr(self, _taxon)
            if value != '---':
                filter_dict["otu__" + _taxon] = getattr(self, _taxon)

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

    def export(self, ids, file_obj_bacteria, file_obj_eukaryotes, file_obj_fungi, file_obj_archea):
        writer_bacteria = csv.writer(file_obj_bacteria)
        writer_eukaryotes = csv.writer(file_obj_eukaryotes)
        writer_fungi = csv.writer(file_obj_fungi)
        writer_archea = csv.writer(file_obj_archea)

        self.field_data = self._get_fields(self.model)

        writer_bacteria.writerow(self._get_headers())
        writer_eukaryotes.writerow(self._get_headers())
        writer_fungi.writerow(self._get_headers())
        writer_archea.writerow(self._get_headers())

        bacteria_count = fungi_count = eukaryotes_count = archea_count = 0

        for row in self._get_rows(ids):
            kingdom = row[3]
            if kingdom == "Bacteria":
                writer_bacteria.writerow(row)
                bacteria_count += 1
            elif kingdom == "Fungi":
                writer_fungi.writerow(row)
                fungi_count += 1
            elif kingdom == "Eukaryote":
                writer_eukaryotes.writerow(row)
                eukaryotes_count += 1
            elif kingdom == 'Archaea':
                writer_archea.writerow(row)
                archea_count += 1
            else:
                logger.info("unknown kingdom?!: %s" % row)
                pass

        file_obj_bacteria.flush()
        file_obj_bacteria.seek(0)

        file_obj_eukaryotes.flush()
        file_obj_eukaryotes.seek(0)

        file_obj_fungi.flush()
        file_obj_fungi.seek(0)

        file_obj_archea.flush()
        file_obj_archea.seek(0)

        if bacteria_count == 0:
            file_obj_bacteria.close()
            file_obj_bacteria = None

        if fungi_count == 0:
            file_obj_fungi.close()
            file_obj_fungi = None

        if eukaryotes_count == 0:
            file_obj_eukaryotes.close()
            file_obj_eukaryotes = None

        if archea_count == 0:
            file_obj_archea.close()
            file_obj_archea = None

        return file_obj_bacteria, file_obj_eukaryotes, file_obj_fungi, file_obj_archea
