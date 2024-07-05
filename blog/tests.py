# from django.test import TestCase
# from .models import MyUser, Post, CommentPost, LikePost, FollowMyUser
# from django.contrib.auth.models import User
#
# class ModelsTestCase(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(username="testuser1")
#         self.user2 = User.objects.create(username="testuser2")
#         self.myuser1 = MyUser.objects.create(user=self.user1)
#         self.myuser2 = MyUser.objects.create(user=self.user2)
#         self.post1 = Post.objects.create(author=self.myuser1)
#         self.post2 = Post.objects.create(author=self.myuser2)
#         self.comment1 = CommentPost.objects.create(author=self.myuser1, post=self.post1, message="Test comment")
#         self.comment2 = CommentPost.objects.create(author=self.myuser2, post=self.post2, message="Another test comment")
#         self.like1 = LikePost.objects.create(author=self.myuser1, post=self.post2)
#         self.follow = FollowMyUser.objects.create(follower=self.myuser1, following=self.myuser2)
#
#     def test_user_creation(self):
#         self.assertEqual(MyUser.objects.count(), 2)
#         self.assertEqual(User.objects.count(), 2)
#
#     def test_post_creation(self):
#         self.assertEqual(Post.objects.count(), 2)
#
#     def test_comment_creation(self):
#         self.assertEqual(CommentPost.objects.count(), 2)
#
#     def test_like_creation(self):
#         self.assertEqual(LikePost.objects.count(), 1)
#
#     def test_follow_creation(self):
#         self.assertEqual(FollowMyUser.objects.count(), 1)
#
#     def test_followed_user_followers_count(self):
#         self.assertEqual(self.myuser2.follower_count, 1)
#
#     def test_following_user_following_count(self):
#         self.assertEqual(self.myuser1.following_count, 1)
#
#     def test_post_like_count_increment(self):
#         initial_like_count = self.post1.like_count
#         self.like2 = LikePost.objects.create(author=self.myuser2, post=self.post1)
#         self.post1.refresh_from_db()
#         self.assertEqual(self.post1.like_count, initial_like_count + 1)
#
#     def test_comment_visibility(self):
#         self.assertTrue(self.comment1.is_visible)
#         self.assertTrue(self.comment2.is_visible)




from django.test import TestCase, Client
from django.urls import reverse
from .models import MyUser, Post, CommentPost, LikePost, FollowMyUser
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.my_user = MyUser.objects.create(user=self.user)
        self.post = Post.objects.create(author=self.my_user)
        self.comment = CommentPost.objects.create(author=self.my_user, post=self.post, message='Test comment')
        self.like = LikePost.objects.create(author=self.my_user, post=self.post)
        self.follow = FollowMyUser.objects.create(follower=self.my_user, following=self.my_user)

    def test_index_view(self):
        # Test index view
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view(self):
        # Test login view
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    # Add more test methods for other views...

    def test_profile_settings_view(self):
        # Test profile settings view
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('profile_settings'), {'profile_picture': SimpleUploadedFile("file.jpg", b"file_content")})
        self.assertEqual(response.status_code, 302)  # Redirects after successful upload
        # Check if profile picture is updated
        updated_user = MyUser.objects.get(user=self.user)
        self.assertTrue(updated_user.profile_picture)

    def test_follow_view(self):
        # Test follow view
        self.client.login(username='testuser', password='testpassword')
        profile_id = self.my_user.id
        response = self.client.get(reverse('follow'), {'profile_id': profile_id})
        self.assertEqual(response.status_code, 302)  # Redirects after follow/unfollow

        # Check if follow/unfollow is working correctly
        follow_exists = FollowMyUser.objects.filter(follower=self.my_user, following_id=profile_id).exists()
        self.assertFalse(follow_exists)  # As the follow should be deleted

    # Add more test methods for other views...
