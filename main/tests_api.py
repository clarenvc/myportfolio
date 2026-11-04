from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Skill


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