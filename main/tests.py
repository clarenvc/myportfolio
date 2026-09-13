from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from main.models import Experience
from main.models import Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

class SkillTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.skills_url = reverse('main:show_skills')

    def test_skills_url_exists_and_uses_correct_template(self):
        response = self.client.get(self.skills_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'skills.html')

    def test_skills_page_empty_state(self):
        response = self.client.get(self.skills_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No skills have been added yet.")

    def test_skills_page_shows_data(self):
        # Buat dummy data
        Skill.objects.create(
            tool_name="Test Tool VS Code",
            category_title="Programming",
            description="Ini adalah deskripsi test."
        )
        response = self.client.get(self.skills_url)
        self.assertEqual(response.status_code, 200)
        # Pastikan data yang baru dibuat muncul di HTML
        self.assertContains(response, "Test Tool VS Code")
        self.assertContains(response, "Ini adalah deskripsi test.")