from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):
    def test_index_view(self):
        """
        Page should display "Projects"
        """
        response = self.client.get(reverse('sgSite:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projects")


class ProjectViewTests(TestCase):
    def test_project_view(self):
        """
        Page should successfully pull up a shot with sequence bunny_010
        """
        url = reverse('sgSite:project', args=[70])
        response = self.client.get(url)
        self.assertContains(response, "bunny_010")
