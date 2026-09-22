from os.path import join
import subprocess
from django.conf import settings
from django.test import TestCase


class TestValidHtml(TestCase):
    def assertValid(self, url):
        """
        Navigate to the internal url and check the html is valid by passing it
        through the W3C validator
        """

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Command to run the W3C validator from standard input
        command = [
            'java',
            '-jar',
            join(settings.VALIDATOR_DIR, 'vnu.jar'),
            '-'
        ]

        result = subprocess.run(
            command,
            input=response.content,
            capture_output=True
        )

        self.assertTrue(
            result.returncode == 0,
            msg="The HTML is not valid\n{0}\n{1}".format
            (
                url,
                result.stderr.decode('utf-8')
            )
        )
