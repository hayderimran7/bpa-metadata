"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'bpam.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'bpam.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for bpam.
    """

    title = "Bioplatforms Australia Metadata"
    columns = 3

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Bioplatforms Australia Projects'),
            exclude=('django.contrib.*', 'apps.bpaauth.*'),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('User Management'),
            models=('apps.bpaauth.*', 'django.contrib.auth.models.Group',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest BioInformatics News'),
            feed_url='http://www.biomedcentral.com/bmcbioinformatics/editorspicks/rss',
            limit=5
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Bioplatforms Australia'),
                    'url': 'http://www.bioplatforms.com.au/',
                    'external': True,
                },
                {
                    'title': _('Bioplatforms Australia ISAtools'),
                    'url': 'http://portal.bioplatforms.com/bioinvindex/browse_studies.seam',
                    'external': True,
                },
                {
                    'title': _('Bioplatforms Australia Archive'),
                    'url': 'https://archive.bioplatforms.com/',
                    'external': True,
                },
                {
                    'title': _('Bioplatforms Australia Public file repository'),
                    'url': 'ftp://files.ivec.org/bpa',
                    'external': True,
                },
                {
                    'title': _('Centre for Comparative Genomics'),
                    'url': 'http://ccg.murdoch.edu.au/index.php/Main_Page',
                    'external': True,
                },
            ]
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for bpam.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
