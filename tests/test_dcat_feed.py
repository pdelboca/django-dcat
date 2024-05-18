from django.test import TestCase
from dcat.models import Agent, Catalog, Dataset

# Create your tests here.


class DCATSerializationJSONLDTestCase(TestCase):

    def setUp(self):
        publisher = Agent.objects.create(
            name='Food and Agriculture Organization of the United Nations',
            type='foaf:Agent'
        )
        catalog = Catalog.objects.create(
            title='FAO Data in Emergencies',
            description='A testing catalog based on true data.',
            publisher=publisher,
            homepage='https://data-in-emergencies.fao.org'
        )

        Dataset.objects.create(
            title='Colombia - Household Questionnaire - Round 3',
            description='Household questionarie',
            catalog=catalog,
        )
        Dataset.objects.create(
            title='Afghanistan - Household Questionnaire - Round 6',
            catalog=catalog,
        )

    def test_agent_to_jsonld(self):
        publisher = Agent.objects.first()
        result = publisher.to_jsonld()
        self.assertEqual(result['@type'], publisher.type)
        self.assertEqual(result['foaf:name'], publisher.name)

    def test_catalog_to_jsonld(self):
        catalog = Catalog.objects.first()
        result = catalog.to_jsonld()

        self.assertEqual(result['@type'], 'dcat:Catalog')
        self.assertEqual(result['dct:title'], catalog.title)
        self.assertEqual(result['dct:description'], catalog.description)
        self.assertEqual(result['dct:publisher'], catalog.publisher.to_jsonld())
        self.assertEqual(result['foaf:homepage'], {'@type': 'foaf:Document', 'foaf:Document': catalog.homepage})
        self.assertEqual(
            result['dcat:dataset'],
            [
                {'dct:title': 'Colombia - Household Questionnaire - Round 3', 'dct:description': 'Household questionarie'},
                {'dct:title': 'Afghanistan - Household Questionnaire - Round 6'}
            ]
        )
