"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper


def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('/', controller='root', action='index')
    map.connect('/index{.format}', controller='root', action='index')

    map.connect('/openid/{action}', controller='openidauth')
    map.connect('/twitter/{action}', controller='twitteroauth')

    map.connect('/user/all', controller='user',
                action='all', conditions=dict(method=['GET']))
    map.connect('/user/{id}/badges{.format}', controller='user',
                action='edit_badges', conditions=dict(method=['GET']))
    map.connect('/user/{id}/badges', controller='user',
                action='update_badges', conditions=dict(method=['POST']))
    # Old dashboard
    map.connect('/user/{id}/dashboard', controller='user',
                action='legacy_dashboard')
    map.connect('/user/{id}/dashboard_proposals', controller='user',
                action='legacy_dashboard_proposals')
    map.connect('/user/{id}/dashboard_pages', controller='user',
                action='legacy_dashboard_pages')

    # New event stream dashboard
    map.connect('/user/dashboard', controller='user',
                action='dashboard')
    map.connect('/user/dashboard/contributions', controller='user',
                action='dashboard_contributions')
    map.connect('/user/dashboard/votes', controller='user',
                action='dashboard_votes')
    map.connect('/user/dashboard/delegations', controller='user',
                action='dashboard_delegations')
    map.connect('/welcome/{id}/{token}', controller='user',
                action='welcome')

    # avatar
    map.connect('/user/{id}_{x}x{y}.png',
                controller='user', action='avatar')
    map.connect('/user/{id}_{y}.png',
                controller='user', action='avatar')

    map.resource('user', 'user', member={'votes': 'GET',
                                         'delegations': 'GET',
                                         'instances': 'GET',
                                         'about': 'GET',
                                         'latest_events': 'GET',
                                         'latest_contributions': 'GET',
                                         'latest_milestones': 'GET',
                                         'latest_votes': 'GET',
                                         'latest_delegations': 'GET',
                                         'watchlist': 'GET',
                                         'groupmod': 'GET',
                                         'ban': 'GET',
                                         'unban': 'GET',
                                         'ask_delete': 'GET',
                                         'revert': 'GET',
                                         'reset': 'GET',
                                         'activate': 'GET',
                                         'resend': 'GET',
                                         'set_password': 'POST',
                                         'generate_welcome_link': 'POST'},
                 collection={'complete': 'GET',
                             'filter': 'GET',
                             # provide user-independent URLs to user settings
                             'redirect_settings': 'GET',
                             'redirect_settings_login': 'GET',
                             'redirect_settings_notifications': 'GET',
                             'redirect_settings_advanced': 'GET',
                             'redirect_settings_optional': 'GET',
                             })

    # TODO work this into a complete subcontroller.
    map.connect('/user/{id}/message.{format}', controller='message',
                action='create',
                conditions=dict(method=['POST', 'PUT']))
    map.connect('/user/{id}/message', controller='message', action='create',
                conditions=dict(method=['POST', 'PUT']))
    map.connect('/user/{id}/message/new.{format}', controller='message',
                action='new',
                conditions=dict(method=['GET']))
    map.connect('/user/{id}/message/new', controller='message', action='new',
                conditions=dict(method=['GET']))
    map.connect('/user/{id}/settings{.format}',
                controller='user', action='settings_personal',
                conditions=dict(method=['GET']))
    map.connect('/user/{id}/settings{.format}',
                controller='user', action='settings_personal_update',
                conditions=dict(method=['PUT']))
    map.connect('/user/{id}/settings/login{.format}',
                controller='user', action='settings_login',
                conditions=dict(method=['GET']))
    map.connect('/user/{id}/settings/login{.format}',
                controller='user', action='settings_login_update',
                conditions=dict(method=['PUT']))
    map.connect('/user/{id}/settings/notifications{.format}',
                controller='user', action='settings_notifications',
                conditions=dict(method=['GET']))
    map.connect('/user/{id}/settings/notifications{.format}',
                controller='user', action='settings_notifications_update',
                conditions=dict(method=['PUT']))
    map.connect('/user/{id}/settings/advanced{.format}',
                controller='user', action='settings_advanced',
                conditions=dict(method=['GET']))
    map.connect('/user/{id}/settings/advanced{.format}',
                controller='user', action='settings_advanced_update',
                conditions=dict(method=['PUT']))
    map.connect('/user/{id}/settings/optional{.format}',
                controller='user', action='settings_optional',
                conditions=dict(method=['GET']))
    map.connect('/user/{id}/settings/optional{.format}',
                controller='user', action='settings_optional_update',
                conditions=dict(method=['PUT']))

    map.connect('/message/new', controller='massmessage', action='new')
    map.connect('/message/preview', controller='massmessage', action='preview')
    map.connect('/message/create', controller='massmessage', action='create')

    map.connect('/register', controller='user', action='new')
    map.connect('/login', controller='user', action='login')
    map.connect('/logout', controller='user', action='logout')
    map.connect('/post_logout', controller='user', action='post_logout')
    map.connect('/post_login', controller='user', action='post_login')
    map.connect('/perform_login', controller='user', action='perform_login')
    map.connect('/reset', controller='user', action='reset_form',
                conditions=dict(method=['GET']))
    map.connect('/reset', controller='user', action='reset_request',
                conditions=dict(method=['POST']))

    #map.connect('/proposal/{id}/badges', controller='proposal',
                #action='badges', conditions=dict(method=['GET']))
    #map.connect('/proposal/{id}/badges', controller='proposal',
                #action='update_badges', conditions=dict(method=['POST']))

    map.resource('proposal', 'proposal', member={'votes': 'GET',
                                                 'delegations': 'GET',
                                                 'activity': 'GET',
                                                 'alternatives': 'GET',
                                                 'ask_delete': 'GET',
                                                 'ask_adopt': 'GET',
                                                 'adopt': 'POST',
                                                 'tag': 'POST',
                                                 'untag': 'GET',
                                                 'badges': 'GET',
                                                 'update_badges': 'POST',
                                                 'history': 'GET'},
                 collection={'filter': 'GET'})
    map.connect('/proposal/{proposal_id}/{selection_id}/details{.format}',
                controller='selection',
                action='details')

    map.resource('implementation', 'implementation', controller='selection',
                 member={'ask_delete': 'GET'},
                 collection={'include': 'GET',
                             'propose': 'GET'},
                 parent_resource=dict(member_name='proposal',
                                      collection_name='proposal'))

    map.connect('/page/diff', controller='page', action='diff',
                conditions=dict(method=['GET']))

    map.connect('/page/{id}/amendment{.format}',
                controller='page',
                action='show', amendment=True,
                conditions=dict(method=['GET']),
                )
    map.connect('/page/{page}/amendment{.format}',
                controller='proposal',
                action='create', amendment=True,
                conditions=dict(method=['POST'])
                )
    map.connect('/page/{page}/amendment/new{.format}',
                controller='proposal',
                action='new', amendment=True,
                conditions=dict(method=['GET']),
                )
    map.connect('/page/{id}/amendment/{variant}{.format}',
                controller='page',
                action='show', amendment=True,
                conditions=dict(method=['GET']),
                )
    map.connect('/page/{page}/amendment/{id}{.format}',
                controller='proposal',
                action='update',
                conditions=dict(method=['PUT'])
                )
    map.connect('/page/{page}/amendment/{id}{.format}',
                controller='proposal',
                action='delete',
                conditions=dict(method=['DELETE'])
                )
    map.connect('/page/{page}/amendment/{id}/edit{.format}',
                controller='proposal',
                action='edit',
                conditions=dict(method=['GET']),
                )
    map.connect('/page/{page}/amendment/{id}/ask_delete{.format}',
                controller='proposal',
                action='ask_delete',
                conditions=dict(method=['GET']),
                )

    map.connect('/page/{id}/{variant}/history{.format}',
                controller='page',
                action='history',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/history{.format}',
                controller='page',
                action='history',
                conditions=dict(method=['GET']),
                )
    map.connect('/page/{id}/comments{.format}',
                controller='page',
                action='comments',
                conditions=dict(method=['GET']),
                )
    map.connect('/page/{id}/{variant}/branch',
                controller='page',
                action='edit',
                branch=True,
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant}/ask_purge',
                controller='page', action='ask_purge',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant}/purge',
                controller='page',
                action='purge',
                conditions=dict(method=['POST', 'DELETE']))
    map.connect('/page/{id};{text}/ask_purge_history',
                controller='page', action='ask_purge_history',
                conditions=dict(method=['GET']))
    map.connect('/page/{id};{text}/purge_history',
                controller='page',
                action='purge_history',
                conditions=dict(method=['POST', 'DELETE']))
    map.connect('/page/{id}/{variant}/edit.{format}',
                controller='page',
                action='edit',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant}/edit', controller='page', action='edit',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/edit.{format}', controller='page', action='edit',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/branch', controller='page', action='edit',
                branch=True,
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/edit', controller='page', action='edit',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/ask_delete{.format}', controller='page',
                action='ask_delete',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant};{text}.{format}', controller='page',
                action='show',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant};{text}/branch', controller='page',
                action='edit', branch=True,
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant};{text}', controller='page',
                action='show',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant}.{format}', controller='page',
                action='show',
                conditions=dict(method=['GET']))
    map.connect('/page/{id}/{variant}', controller='page', action='show',
                conditions=dict(method=['GET']))
    map.connect('/page/{id};{text}.{format}', controller='page', action='show',
                conditions=dict(method=['GET']))
    map.connect('/page/{id};{text}/branch', controller='page', action='edit',
                branch=True,
                conditions=dict(method=['GET']))
    map.connect('/page/{id};{text}', controller='page', action='show',
                conditions=dict(method=['GET']))

    map.resource('page', 'page', member={'ask_delete': 'GET'})

    #map.connect('/adopted', controller='proposal', action='adopted')

    map.resource('comment', 'comment', member={'history': 'GET',
                                               'revert': 'GET',
                                               'purge_history': 'GET',
                                               'ask_delete': 'GET'})

    map.connect('/comment/form/edit/{id}', controller='comment',
                action='edit_form')
    map.connect('/comment/form/create/{topic}', controller='comment',
                action='create_form', variant=None)
    map.connect('/comment/form/reply/{id}', controller='comment',
                action='reply_form')

    map.resource('milestone', 'milestone', member={'ask_delete': 'GET'})

    map.connect('/poll/{id}/rate{.format}', controller='poll', action='rate',
                conditions=dict(method=['GET', 'POST']))

    map.connect('/poll/{id}/widget{.format}', controller='poll',
                action='widget', conditions=dict(method=['GET', 'POST']))

    map.connect('/poll/{id}/vote{.format}', controller='poll', action='vote',
                conditions=dict(method=['GET', 'POST']))

    map.resource('poll', 'poll', member={'votes': 'GET',
                                         'ask_delete': 'GET',
                                         'widget': 'GET'})

    map.connect('/badge{.format}', controller='badge', action='index',
                conditions=dict(method=['GET']))
    map.connect('/badge/{badge_type}/add{.format}', controller='badge',
                action='add', conditions=dict(method=['GET']))
    map.connect('/badge/{badge_type}/add{.format}', controller='badge',
                action='create', conditions=dict(method=['POST']))
    map.connect('/badge/edit/{id}{.format}', controller='badge',
                action="edit", conditions=dict(method=['GET']))
    map.connect('/badge/edit/{id}{.format}',
                controller='badge', action="update",
                conditions=dict(method=['POST']))
    map.connect('/badge/delete/{id}{.format}',
                controller='badge', action="ask_delete",
                conditions=dict(method=['GET']))
    map.connect('/badge/delete/{id}',
                controller='badge', action="delete",
                conditions=dict(method=['POST']))

    # not using REST since tags may contain dots, thus failing format
    # detection.
    map.connect('/tag', controller='tag', action='index',
                conditions=dict(method=['GET']))
    map.connect('/tag', controller='tag', action='create',
                conditions=dict(method=['POST']))
    map.connect('/tag/autocomplete', controller='tag', action='autocomplete')
    map.connect('/untag', controller='tag', action='untag')
    map.connect('/untag_all', controller='tag', action='untag_all')
    map.connect('/tag/{id}', controller='tag', action='show')

    map.resource('delegation', 'delegation')
    #map.resource('delegations', 'delegation')

    map.connect('/d/{id}', controller='root', action='dispatch_delegateable')
    map.connect('/sitemap.xml', controller='root', action='sitemap_xml')
    map.connect('/robots.txt', controller='root', action='robots_txt')
    map.connect('/feed.rss', controller='root', action='index', format='rss')
    map.connect('/tutorials', controller='root', action='tutorials')

    map.connect('/search/filter', controller='search', action='filter')
    map.connect('/search{.format}', controller='search', action='query')

    map.connect('/abuse/report', controller='abuse', action='report')
    map.connect('/abuse/new', controller='abuse', action='new')

    map.connect('/instance/{id}_{x}x{y}.png',
                controller='instance', action='icon')
    map.connect('/instance/{id}_{y}.png',
                controller='instance', action='icon')
    map.connect('/instance/{id}/settings{.format}',
                controller='instance', action='settings_general',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings{.format}',
                controller='instance', action='settings_general_update',
                conditions=dict(method=['PUT']))
    map.connect('/instance/{id}/settings/appearance{.format}',
                controller='instance', action='settings_appearance',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/appearance{.format}',
                controller='instance', action='settings_appearance_update',
                conditions=dict(method=['PUT']))
    map.connect('/instance/{id}/settings/contents{.format}',
                controller='instance', action='settings_contents',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/contents{.format}',
                controller='instance', action='settings_contents_update',
                conditions=dict(method=['PUT']))
    map.connect('/instance/{id}/settings/voting{.format}',
                controller='instance', action='settings_voting',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/voting{.format}',
                controller='instance', action='settings_voting_update',
                conditions=dict(method=['PUT']))
    map.connect('/instance/{id}/settings/badges{.format}',
                controller='instance', action='settings_badges',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/badges{.format}',
                controller='instance', action='settings_badges_update',
                conditions=dict(method=['PUT']))
    map.connect('/instance/{id}/settings/badges/{badge_type}/add{.format}',
                controller='instance',
                action='settings_badges_add', conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/badges/{badge_type}/add{.format}',
                controller='instance',
                action='settings_badges_create',
                conditions=dict(method=['POST']))
    map.connect('/instance/{id}/settings/badges/edit/{badge_id}{.format}',
                controller='instance',
                action="settings_badges_edit", conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/badges/edit/{badge_id}{.format}',
                controller='instance', action="settings_badges_update",
                conditions=dict(method=['POST']))
    map.connect('/instance/{id}/settings/badges/delete/{badge_id}{.format}',
                controller='instance', action="settings_badges_ask_delete",
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/badges/delete/{badge_id}{.format}',
                controller='instance', action="settings_badges_delete",
                conditions=dict(method=['POST']))
    map.connect('/instance/{id}/message/new{.format}',
                controller='massmessage', action='new',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/message{.format}',
                controller='massmessage', action='create',
                conditions=dict(method=['POST']))
    map.connect('/instance/{id}/message/preview{.format}',
                controller='massmessage', action='preview',
                conditions=dict(method=['POST']))
    map.connect('/instance/{id}/members_import{.format}',
                controller='instance', action='members_import',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/members_import{.format}',
                controller='instance', action='members_import_save',
                conditions=dict(method=['PUT', 'POST']))
    map.connect('/instance/{id}/settings/presets{.format}',
                controller='instance', action='settings_presets',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/settings/presets{.format}',
                controller='instance', action='settings_presets_update',
                conditions=dict(method=['PUT', 'POST']))
    map.connect('/instance/{id}/presets{.format}',
                controller='instance', action='presets',
                conditions=dict(method=['GET']))
    map.connect('/instance/{id}/presets{.format}',
                controller='instance', action='presets_update',
                conditions=dict(method=['POST']))

    map.resource('instance', 'instance', member={'join': 'GET',
                                                 'leave': 'POST',
                                                 'filter': 'GET',
                                                 'ask_leave': 'GET',
                                                 'ask_delete': 'GET',
                                                 'style': 'GET',
                                                 'badges': 'GET',
                                                 'update_badges': 'POST',
                                                 'activity': 'GET'})

    map.connect('/stats/', controller='stats')

    map.connect('/admin', controller='admin', action="index")
    map.connect('/admin/users/import{.format}', controller='admin',
                action="user_import", conditions=dict(method=['POST']))
    map.connect('/admin/users/import{.format}', controller='admin',
                action="user_import_form", conditions=dict(method=['GET']))
    map.connect('/admin/export',
                controller='admin', action='export_dialog')
    map.connect('/admin/export/do',
                controller='admin', action='export_do')
    map.connect('/admin/import{.format}',
                controller='admin', action='import_dialog')
    map.connect('/admin/import/do',
                controller='admin', action='import_do')
    map.connect('/admin/treatment/',
                controller='treatment', action='index',
                conditions={'method': 'GET'},)
    map.connect('/admin/treatment/',
                controller='treatment', action='create',
                conditions={'method': 'POST'},)
    map.connect('/admin/treatment/{key}/assign',
                controller='treatment', action='assign',
                conditions={'method': 'POST'},)
    map.connect('/admin/treatment/{key}/assigned',
                controller='treatment', action='assigned')

    map.connect('/static{.format}', controller='static', action='index',
                conditions=dict(method=['GET', 'HEAD']))
    map.connect('/static{.format}', controller='static', action='make_new',
                conditions=dict(method=['POST']))
    map.connect('/static/new{.format}', controller='static', action='new')
    map.connect('/static/edit/{lang}/*key',
                controller='static', action='edit',
                conditions=dict(method=['GET', 'HEAD']))
    map.connect('/static/edit/{lang}/*(key){.format}',
                controller='static', action='update',
                conditions=dict(method=['POST']))
    map.connect('/static/*(key){.format}', controller='static',
                action='serve')
    map.connect('/outgoing_link/{url_enc}', controller='redirect',
                action='outgoing_link',
                conditions=dict(method=['GET', 'HEAD']))

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
