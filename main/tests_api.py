from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from main.models import Skill, Experience, Education


class SkillAPITestCase(APITestCase):

    def setUp(self):
        # 1. Buat Superuser & User Biasa untuk simulasi hak akses
        self.superuser = User.objects.create_superuser(
            username="admin", password="password123"
        )
        self.normal_user = User.objects.create_user(
            username="user biasa", password="password123"
        )

        # 2. Buat data Skill awal di database
        self.skill = Skill.objects.create(
            tool_name="Python",
            category_title="Programming Language",
            description="Bahasa pemrograman utama untuk Django.",
            sub_skills="Django, DRF",
        )

        # 3. Definisikan URL API
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", kwargs={"skill_id": self.skill.id})
        self.star_url = reverse("api:skill-star", kwargs={"skill_id": self.skill.id})

    def test_get_skill_list(self):
        """Memastikan siapa pun (bahkan tanpa login) bisa melihat daftar skill (200 OK)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["tool_name"], "Python")

    def test_create_skill_as_superuser(self):
        """Memastikan superuser bisa menambahkan skill baru (201 Created)."""
        self.client.force_authenticate(user=self.superuser)
        payload = {
            "tool_name": "Docker",
            "category_title": "DevOps",
            "description": "Containerization tool",
            "sub_skills": "Dockerfile, Compose",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 2)

    def test_create_skill_as_normal_user_forbidden(self):
        """Memastikan user biasa DITOLAK saat mencoba tambah skill (403 Forbidden)."""
        self.client.force_authenticate(user=self.normal_user)
        payload = {
            "tool_name": "Hacker Tool",
            "category_title": "Security",
            "description": "Ilegal",
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_skill_as_superuser(self):
        """Memastikan superuser bisa menghapus skill (204 No Content)."""
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.count(), 0)

    def test_toggle_star_skill(self):
        """Memastikan user terautentikasi bisa melakukan toggle star pada skill."""
        self.client.force_authenticate(user=self.normal_user)

        # Star pertama kali (Tambahkan star)
        response_1 = self.client.post(self.star_url)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertTrue(response_1.data["is_starred"])
        self.assertEqual(response_1.data["star_count"], 1)

        # Star kedua kali (Unstar)
        response_2 = self.client.post(self.star_url)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertFalse(response_2.data["is_starred"])
        self.assertEqual(response_2.data["star_count"], 0)

class ExperienceAPITestCase(APITestCase):
    
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin", password="password123"
        )
        self.normal_user = User.objects.create_user(
            username="userbiasa", password="password123"
        )
        self.editor_user = User.objects.create_user(
            username="editor", password="password123"
        )
        
        editor_group, created = Group.objects.get_or_create(name="Editor")
        self.editor_user.groups.add(editor_group)

        # Buat data dummy 
        self.experience = Experience.objects.create(
            category="Internship",
            title="Software Engineer Intern",
            description="Developing web applications.",
            is_ongoing=False
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", kwargs={"experience_id": self.experience.id})
        self.star_url = reverse("api:experience-star", kwargs={"experience_id": self.experience.id})

    # --- Test Read-Only ---
    def test_get_experience_list_as_visitor(self):
        """Memastikan pengunjung bisa melihat daftar (200 OK)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_experience_as_visitor_forbidden(self):
        """Memastikan pengunjung ditolak menambah data (403)."""
        payload = {"category": "Job", "title": "Dev", "description": "test", "is_ongoing": False}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Test for Normal User ---
    def test_normal_user_toggle_star(self):
        """Memastikan Normal User bisa toggle star (200 OK)."""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])

    def test_normal_user_delete_forbidden(self):
        """Memastikan Normal User ditolak saat menghapus data (403). Database tidak berubah."""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1) # Data tetap 1

    # --- Test for Editor ---
    def test_editor_patch_allowed(self):
        """Memastikan Editor diizinkan mengubah (PATCH) data (200 OK)."""
        self.client.force_authenticate(user=self.editor_user)
        payload = {"title": "Senior Dev"}
        response = self.client.patch(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Senior Dev")

    def test_editor_post_forbidden(self):
        """Memastikan Editor DITOLAK saat membuat data baru (403)."""
        self.client.force_authenticate(user=self.editor_user)
        payload = {"category": "Job", "title": "Dev", "description": "test", "is_ongoing": False}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1) # Tetap 1

    # --- Test for Superuser ---
    def test_superuser_crud_allowed(self):
        """Memastikan Superuser bisa CRUD (201 Created & 204 No Content)."""
        self.client.force_authenticate(user=self.superuser)
        payload = {"category": "Job", "title": "Admin", "description": "test", "is_ongoing": True}
        response_post = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)

        response_del = self.client.delete(self.detail_url)
        self.assertEqual(response_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Experience.objects.count(), 1)

    # --- Ujian CSRF ---
    def test_csrf_protection_without_token(self):
        """Memastikan permintaan berpotensi bahaya tanpa token CSRF akan ditolak (403)."""
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="admin", password="password123")
        
        payload = {"category": "Job", "title": "Hacker", "description": "test", "is_ongoing": False}
        response = client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)