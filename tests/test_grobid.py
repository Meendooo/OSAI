import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tei_analyzer import parse_tei_xml  # Directo, sin 'src.'

class TestGROBIDAnalysis(unittest.TestCase):
    
    def setUp(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sample_tei = os.path.join(self.root_dir, "data", "processed", "paper1.tei.xml")
    
    def test_parse_tei_xml_structure(self):
        """Verifica que parse_tei_xml devuelve diccionario correcto"""
        if not os.path.exists(self.sample_tei):
            self.skipTest("Sample TEI file not found")
        
        result = parse_tei_xml(self.sample_tei)
        self.assertIsInstance(result, dict)
        self.assertIn('filename', result)
        self.assertIn('abstract', result)
        self.assertIn('num_figures', result)
        self.assertIsInstance(result['num_figures'], int)
        self.assertGreaterEqual(result['num_figures'], 0)
    
    def test_parse_tei_xml_links(self):
        """Verifica que extrae links válidos"""
        if not os.path.exists(self.sample_tei):
            self.skipTest("Sample TEI file not found")
        
        result = parse_tei_xml(self.sample_tei)
        links = result.get('links', [])
        self.assertIsInstance(links, list)
        for link in links:
            self.assertTrue(link.startswith(('http://', 'https://')))

if __name__ == '__main__':
    unittest.main()
