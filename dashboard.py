# -*- coding: utf-8 -*-


from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for navaz.
    """
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
                #[u'Менеджер файлов', '/admin/filebrowser/browse/'],
                #[u'Настройки сайта', '/settings/MyApp'],
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))
        
        
        self.children.append(
            modules.ModelList(
                title = u'Статические страницы сайта',
                models=(
                    'pages.models.Page',
                ),
            )
        )
        
        self.children.append(
            modules.ModelList(
                title = u'Статьи',
                models=(
                    'blog.models.Category',
                    'blog.models.Article',
                    'blog.models.ArticleTag',
                ),
            )
        )
        
        self.children.append(
            modules.ModelList(
                title = u'Архив',
                models=(
                    'archive.models.Specialty',
                    'archive.models.FileType',
                    'archive.models.ArchiveFile',
                ),
            )
        )
        
        self.children.append(
            modules.ModelList(
                title = u'МедиаФайлы',
                models=(
                    'feincms.module.medialibrary.*',
                ),
            )
        )


        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        self.children.append(
            modules.ModelList(
                title = u'Пользователи',
                models=(
                    'django.contrib.auth.*',
                    'users.models.Profile',
                ),
            )
        )
        


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for navaz.
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
