from django.test import TestCase
from home.models import Mailing, Batch
from tracking.models import MailSeen

class MailSeenTest(TestCase):
    def test_total_recipients(self):
        mailing = Mailing.objects.create(email="test@example.com", subject="Test Subject")
        batch1 = Batch.objects.create(name="Batch 1", recipients="email1@example.com,email2@example.com")
        batch2 = Batch.objects.create(name="Batch 2", recipients="email3@example.com,email4@example.com")
        mailing.batches.add(batch1, batch2)

        mail_seen = MailSeen.objects.create(mailing_id=mailing)

        self.assertEqual(mail_seen.total_recipients(), 4)
