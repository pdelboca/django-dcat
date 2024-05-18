from django.test import TestCase
from dcat.models import Agent, Catalog
# Create your tests here.


class DCATExportTestCase(TestCase):

    def setUp(self):
        publisher = Agent.objects.create(
            name='Food and Agriculture Organization of the United Nations',
            type='foaf:Agent'
        )
        Catalog.objects.create(
            title='FAO Data in Emergencies',
            description='A testing catalog based on true data.',
            publisher=publisher
        )

    def test_agent_to_dcat(self):
        publisher = Agent.objects.first()
        result = publisher.to_dcat()
        self.assertEqual(result['@type'], publisher.type)
        self.assertEqual(result['foaf:name'], publisher.name)

    def test_catalog_to_dcat(self):
        catalog = Catalog.objects.first()
        result = catalog.to_dcat()

        self.assertEqual(result['dct:title'], catalog.title)
        self.assertEqual(result['dct:description'], catalog.description)
        self.assertEqual(result['dct:publisher'], catalog.publisher.to_dcat())
