from django.test import TestCase
from dcat.models import Agent, Catalog, Dataset, Distribution


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

        dataset = Dataset.objects.create(
            title='Colombia - Household Questionnaire - Round 3',
            description='Household questionarie',
            catalog=catalog,
        )
        Dataset.objects.create(
            title='Afghanistan - Household Questionnaire - Round 6',
            catalog=catalog,
        )

        Distribution.objects.create(
            dataset=dataset,
            title='ArcGIS Hub Dataset',
            description='Web page',
            external_access_url='https://external.com/distribution/webpage'
        )

        Distribution.objects.create(
            dataset=dataset,
            title='ArcGIS GeoService',
            description='Esri REST',
            external_access_url='https://external.com/distribution/rest'
        )

    def test_distribution_to_jsonld(self):
        distribution = Distribution.objects.first()
        result = distribution.to_jsonld()
        self.assertEqual(result['@type'], 'dcat:Distribution')
        self.assertEqual(result['dcat:accessURL'], distribution.access_url)
        self.assertEqual(result['dct:title'], distribution.title)
        self.assertEqual(result['dct:description'], distribution.description)

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
            result['dcat:dataset'][0],
            {
                'dct:title': 'Colombia - Household Questionnaire - Round 3',
                'dct:description': 'Household questionarie',
                'dcat:distribution': [{
                    '@type': 'dcat:Distribution',
                    'dcat:accessURL': 'https://external.com/distribution/webpage',
                    'dct:title': 'ArcGIS Hub Dataset',
                    'dct:description': 'Web page'
                }, {
                    '@type': 'dcat:Distribution',
                    'dcat:accessURL': 'https://external.com/distribution/rest',
                    'dct:title': 'ArcGIS GeoService',
                    'dct:description': 'Esri REST'
                }]
            },
        )
