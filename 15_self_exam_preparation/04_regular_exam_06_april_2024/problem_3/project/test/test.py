from unittest import TestCase, main

from project.social_media import SocialMedia


class TestSocialMedia(TestCase):
    def setUp(self):
        self.social_media_one = SocialMedia("User One", 'Instagram', 357, "Health")
        self.social_media_two = SocialMedia("User Two", 'YouTube', 157, "Entertainment")
        self.social_media_three = SocialMedia("User Three", 'Twitter', 240, "Sport")

    def test_init(self):
        self.assertEqual("User One", self.social_media_one._username)
        self.assertEqual('Instagram', self.social_media_one._platform)
        self.assertEqual(357, self.social_media_one._followers)
        self.assertEqual("Health", self.social_media_one._content_type)
        self.assertEqual([], self.social_media_one._posts)

    def test_followers_validation_negative(self):
        with self.assertRaises(ValueError) as e:
            self.social_media_one.followers = -1
        self.assertEqual("Followers cannot be negative.", str(e.exception))

    def test_followers_validation_positive(self):
        self.social_media_one.followers = 200
        self.assertEqual(200, self.social_media_one._followers)

    def test_validate_and_set_platform_valid(self):
        self.social_media_one.platform = "YouTube"
        self.assertEqual("YouTube", self.social_media_one.platform)

    def test_validate_and_set_platform(self):
        with self.assertRaises(ValueError) as e:
            self.social_media_one._validate_and_set_platform("Facebook")
        self.assertEqual("Platform should be one of ['Instagram', 'YouTube', 'Twitter']", str(e.exception))

    def test_validate_and_set_platform_empty_string(self):
        with self.assertRaises(ValueError) as e:
            self.social_media_one._validate_and_set_platform("")
        self.assertEqual("Platform should be one of ['Instagram', 'YouTube', 'Twitter']", str(e.exception))

    def test_create_post_valid(self):
        result = self.social_media_one.create_post("Post One")
        self.assertEqual(1, len(self.social_media_one._posts))
        self.assertIn("Post One", self.social_media_one._posts[0]["content"])
        self.assertEqual("New Health post created by User One on Instagram.", result)
        self.assertEqual({'content': 'Post One', 'likes': 0, 'comments': []}, self.social_media_one._posts[0])

    def test_like_post_valid(self):
        self.social_media_one.create_post("Post One")
        result = self.social_media_one.like_post(0)
        self.assertEqual(1, self.social_media_one._posts[0]["likes"])
        self.assertEqual("Post liked by User One.", result)

    def test_like_post_max_valid(self):
        self.social_media_one.create_post("Post One")
        self.social_media_one._posts[0]["likes"] = 10
        result = self.social_media_one.like_post(0)
        self.assertEqual("Post has reached the maximum number of likes.", result)

    def test_like_post_invalid_index(self):
        result = self.social_media_one.like_post(99)
        self.assertEqual("Invalid post index.", result)

    def test_comment_on_post_valid(self):
        self.social_media_one.create_post("Post to comment on.")
        result = self.social_media_one.comment_on_post(0, "This is a long enough comment.")
        self.assertEqual("Comment added by User One on the post.", result)
        self.assertEqual(1, len(self.social_media_one._posts[0]['comments']))
        self.assertEqual({'user': 'User One', 'comment': "This is a long enough comment."},
                         self.social_media_one._posts[0]['comments'][0])

    def test_comment_on_post_short_comment(self):
        self.social_media_one.create_post("Short comment post.")
        result = self.social_media_one.comment_on_post(0, "Too short")
        self.assertEqual("Comment should be more than 10 characters.", result)
        self.assertEqual(0, len(self.social_media_one._posts[0]['comments']))



if __name__ == "__main__":
    main()