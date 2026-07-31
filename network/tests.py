from django.test import TestCase
from django.urls import reverse

from .models import Follow, Like, Post, User


class NetworkSpecTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="pass123")
        self.bob = User.objects.create_user(username="bob", password="pass123")
        self.charlie = User.objects.create_user(username="charlie", password="pass123")

    def test_index_is_public(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Posts")

    def test_profile_shows_follower_and_following_counts(self):
        Follow.objects.create(follower=self.bob, user=self.alice)
        Follow.objects.create(follower=self.charlie, user=self.alice)
        Follow.objects.create(follower=self.alice, user=self.bob)

        response = self.client.get(reverse("profile", args=[self.alice.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Followers: 2")
        self.assertContains(response, "Following: 1")

    def test_like_toggle_updates_count(self):
        post = Post.objects.create(user=self.alice, content="hello")
        self.client.login(username="bob", password="pass123")

        response = self.client.post(reverse("toggle_like", args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["likes"], 1)

        response = self.client.post(reverse("toggle_like", args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["likes"], 0)

    def test_following_page_requires_login(self):
        response = self.client.get(reverse("following"))
        self.assertEqual(response.status_code, 302)
