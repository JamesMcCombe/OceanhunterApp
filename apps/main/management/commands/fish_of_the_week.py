from open_facebook import OpenFacebook

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

from apps.accounts.models import FacebookAdminToken
from apps.main.models import Fish


settings.PAGE_ID = '1482028545461176'


class Command(NoArgsCommand):
    def set_page_token(self):
        token = FacebookAdminToken.objects.last()
        auth_token = token.access_token

        graph = OpenFacebook(auth_token)
        result = graph.get('me/accounts')
        for row in result['data']:
            if row['id'] == settings.PAGE_ID:
                self.page_token = row['access_token']
                print('Page Token: ', self.page_token, ' ***')
                break

    def post_catch_of_the_week(self):
        fish = self.queryset.first()

        graph = OpenFacebook(self.page_token)

        img_url = '{}{}'.format(settings.BASE_URL, fish.image.url)

        url = '{}{}'.format(settings.BASE_URL, reverse('fish_enlarge', args=[fish.pk]))
        message = 'Fish of the week - {} {}kg. '.format(fish.species.name, fish.weight)
        graph.set('me/feed', picture=img_url, link=url, message=message)

    def post_weekly_gallery(self):
        graph = OpenFacebook(self.page_token)

        # resp = graph.set('me/albums', name='Week 12', privacy={'value': 'SELF'})
        # album_id = resp['id']
        album_id = '1482194405444590'

        graph_url = '{}/photos'.format(album_id)

        for fish in self.queryset:
            img_url = '{}{}'.format(settings.BASE_URL, fish.image.url)
            url = '{}{}'.format(settings.BASE_URL, reverse('fish_enlarge', args=[fish.pk]))
            resp = graph.set(graph_url, url=img_url, link=url)

    def handle(self, *args, **options):
        now = timezone.now()

        # assert now.weekday() == 0

        last_week = now - timezone.timedelta(days=7)
        start_of_last_week = last_week.date()
        end_of_last_week = start_of_last_week + timezone.timedelta(days=7)

        self.queryset = Fish.objects.filter(create__gte=start_of_last_week,
                                            create__lt=end_of_last_week).order_by('-points')
        self.set_page_token()

        self.post_catch_of_the_week()
        # self.post_weekly_gallery()


