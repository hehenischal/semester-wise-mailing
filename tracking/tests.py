from django.test import TestCase
from home.models import Mailing, Batch
from tracking.models import MailSeen
from django.urls import reverse

class MailSeenTest(TestCase):
    def test_total_recipients(self):
        mailing = Mailing.objects.create(email="test@example.com", subject="Test Subject")
        batch1 = Batch.objects.create(name="Batch 1", recipients="email1@example.com,email2@example.com")
        batch2 = Batch.objects.create(name="Batch 2", recipients="email3@example.com,email4@example.com")
        mailing.batches.add(batch1, batch2)

        mail_seen = MailSeen.objects.create(mailing_id=mailing)
        self.assertEqual(mail_seen.total_recipients(), 4)


class MailTrackingTest(TestCase):
    def test_mail_tracking(self):
        mailing = Mailing.objects.create(email="test@example.com", subject="Test Subject")
        batch1 = Batch.objects.create(name="Batch 1", recipients="email1@example.com,email2@example.com")
        batch2 = Batch.objects.create(name="Batch 2", recipients="email3@example.com,email4@example.com")
        mailing.batches.add(batch1, batch2)

        mail_seen = MailSeen.objects.create(mailing_id=mailing)
        mail_seen.save()
        print(mail_seen)
        image = self.client.get(reverse('track', kwargs={'token': mail_seen.token}))
        if image:
            self.assertEqual(mail_seen.count, 2)
        else:
            self.assertEqual(mail_seen.count, 0)

        self.assertEqual(mail_seen.total_recipients(), 4)
