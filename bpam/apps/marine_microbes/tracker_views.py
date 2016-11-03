from django.http import Http404
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from models import MetagenomicsTrack, Amplicon16STrack, Amplicon18STrack
from collections import OrderedDict


class TrackOverview(TemplateView):
    template_name = 'marine_microbes/track_overview.html'

    def get_context_data(self, **kwargs):
        context = super(TrackOverview, self).get_context_data(**kwargs)
        return context


class TrackOverviewConstraints(View):
    constraint_queries = OrderedDict([
        ('Metagenomics', lambda: MetagenomicsTrack.objects.all()),
        ('Amplicon 16S', lambda: Amplicon16STrack.objects.all()),
        ('Amplicon 18S', lambda: Amplicon18STrack.objects.all())
    ])
    state_queries = OrderedDict([
        ('generated', ('Generated', None)),
        ('quality', ('Quality Checked', None)),
        ('mindata', ('Minimum Contextual Data Received', None)),
        ('fulldata', ('Full Contextual Data Received', lambda q: q.all())),
        ('all', (None, lambda q: q.all()))
    ])

    def get(self, request):
        tree = []

        for const, const_query in TrackOverviewConstraints.constraint_queries.items():
            const_result = const_query()
            tree.append({"id": const, "parent": "#", "text": "%s (%d)" % (const, len(const_result))})
            for slug, (status, query) in TrackOverviewConstraints.state_queries.items():
                if status is None:
                    continue
                if query:
                    status_count = len(query(const_result))
                    tree.append({"id": "%s/%s" % (const, slug), "parent": const, "text": "%s (%d)" % (status, status_count)})
                else:
                    tree.append({"id": "%s/%s" % (const, slug), "parent": const, "text": "%s (%d)" % (status, 0)})

        return JsonResponse(tree, safe=False)


class TrackDetails(View):

    def get(self, request, constraint=None, status=None):

        if not constraint and not status:
            raise Http404("No constraint or status provided")

        constraint_q = TrackOverviewConstraints.constraint_queries[constraint]
        _, status_q = TrackOverviewConstraints.state_queries[status]

        result = []
        if status_q:
            result = status_q(constraint_q())

        for r in result:
            r.data_type = r.get_data_type_display()

        json_data = self.to_json(result)

        return JsonResponse(json_data, safe=False)

    def to_json(self, raw_data):
        from django.core import serializers
        json_data = serializers.serialize("json", raw_data)

        return json_data
