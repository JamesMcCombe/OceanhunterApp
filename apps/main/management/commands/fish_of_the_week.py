from social_core.backends.facebook import FacebookOAuth2
from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import FacebookAdminToken
from apps.main.models import Fish


class Command(BaseCommand):
    def set_page_token(self):
        token = FacebookAdminToken.objects.last()
        auth_token = token.access_token

        backend = FacebookOAuth2()
        result = backend.get_json('https://graph.facebook.com/me/accounts', params={'access_token': auth_token})

        for row in result['data']:
            if row['id'] == settings.PAGE_ID:
                self.page_token = row['access_token']
                print('Page Token: ', self.page_token, ' ***')
                break

    def post_catch_of_the_week(self):
        fish = self.queryset.first()

        backend = FacebookOAuth2()
        graph_url = 'https://graph.facebook.com/me/feed'

        img_url = f'{settings.BASE_URL}{fish.image.url}'
        url = f'{settings.BASE_URL}{reverse("fish_enlarge", args=[fish.pk])}'
        message = f'Crayfish of the week - {fish.species.name} {fish.weight}kg.'

        backend.get_json(graph_url, method='POST', params={
            'picture': img_url,
            'link': url,
            'message': message,
            'access_token': self.page_token
        })

    def post_weekly_gallery(self):
        backend = FacebookOAuth2()
        album_resp = backend.get_json('https://graph.facebook.com/me/albums', method='POST', params={
            'name': f'Week {timezone.now().strftime("%W")}',
            'privacy': {'value': 'SELF'},
            'access_token': self.page_token
        })

        album_id = album_resp['id']
        graph_url = f'https://graph.facebook.com/{album_id}/photos'

        for fish in self.queryset:
            img_url = f'{settings.BASE_URL}{fish.image.url}'
            url = f'{settings.BASE_URL}{reverse("fish_enlarge", args=[fish.pk])}'
            backend.get_json(graph_url, method='POST', params={
                'url': img_url,
                'link': url,
                'access_token': self.page_token
            })

    def handle(self, *args, **options):
        now = timezone.now()
        last_week = now - timezone.timedelta(days=7)
        start_of_last_week = last_week.date()
        end_of_last_week = start_of_last_week + timezone.timedelta(days=7)

        self.queryset = Fish.objects.filter(
            create__gte=start_of_last_week,
            create__lt=end_of_last_week
        ).order_by('-points')

        self.set_page_token()
        self.post_catch_of_the_week()
        self.post_weekly_gallery()
