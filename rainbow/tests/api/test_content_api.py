"""API tests for the read-only content endpoints: texts and news.

Both require authentication, are read-only (GET/HEAD/OPTIONS), and news only
exposes published items.
"""
import pytest
from model_bakery import baker

pytestmark = pytest.mark.django_db

TEXTS_URL = '/api/texts/'
NEWS_URL = '/api/news/'


# --- texts ----------------------------------------------------------------

def test_texts_require_authentication(api_client):
    response = api_client.get(TEXTS_URL)
    assert response.status_code in (401, 403)


def test_texts_list_and_retrieve(auth_client, user):
    text = baker.make('texts.Text')

    client = auth_client(user)
    list_response = client.get(TEXTS_URL)
    detail_response = client.get(f'{TEXTS_URL}{text.uuid}/')

    assert list_response.status_code == 200
    assert str(text.uuid) in [item['uuid'] for item in list_response.data]
    assert detail_response.status_code == 200
    assert detail_response.data['uuid'] == str(text.uuid)


def test_texts_are_read_only(auth_client, user):
    response = auth_client(user).post(TEXTS_URL, {'title': 'x', 'body': 'y', 'notes': 'z'})
    assert response.status_code == 405


# --- news -----------------------------------------------------------------

def test_news_require_authentication(api_client):
    response = api_client.get(NEWS_URL)
    assert response.status_code in (401, 403)


def test_news_lists_only_published(auth_client, user):
    published = baker.make('news.NewsItem', published=True, title='published')
    baker.make('news.NewsItem', published=False, title='draft')

    response = auth_client(user).get(NEWS_URL)

    assert response.status_code == 200
    titles = [item['title'] for item in response.data]
    assert 'published' in titles
    assert 'draft' not in titles


def test_news_unpublished_item_is_not_retrievable(auth_client, user):
    draft = baker.make('news.NewsItem', published=False)

    response = auth_client(user).get(f'{NEWS_URL}{draft.uuid}/')

    assert response.status_code == 404


def test_news_is_read_only(auth_client, user):
    response = auth_client(user).post(NEWS_URL, {'title': 'x', 'body': 'y'})
    assert response.status_code == 405
