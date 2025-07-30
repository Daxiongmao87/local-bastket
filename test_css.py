#!/usr/bin/env python3
"""
CSS Testing Framework for Local Basket
Automated testing for CSS builds, linting, and performance
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

class CSSTestFramework(unittest.TestCase):
    """Test framework for CSS architecture and build system"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.css_dir = Path("static/css")
        cls.build_dir = Path("static/build")
        cls.required_files = [
            "static/css/variables.css",
            "static/css/base.css", 
            "static/css/main.css",
            "static/css/design-system.css",
            "static/css/components-v2.css",
            "static/css/accessibility.css"
        ]
        
    def test_required_css_files_exist(self):
        """Test that all required CSS files exist"""
        for file_path in self.required_files:
            with self.subTest(file=file_path):
                self.assertTrue(Path(file_path).exists(), 
                              f"Required CSS file missing: {file_path}")
    
    def test_css_build_system(self):
        """Test that CSS build system works correctly"""
        # Run build
        result = subprocess.run(['python', 'build_css.py'], 
                              capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, 
                        f"CSS build failed: {result.stderr}")
        
        # Check that build files were created
        expected_build_files = [
            "static/build/bundle.min.css",
            "static/build/fontawesome-subset.min.css", 
            "static/build/critical.min.css"
        ]
        
        for build_file in expected_build_files:
            with self.subTest(file=build_file):
                self.assertTrue(Path(build_file).exists(),
                              f"Build file not created: {build_file}")
    
    def test_css_file_sizes(self):
        """Test that CSS files are within reasonable size limits"""
        size_limits = {
            "static/css/base.css": 10 * 1024,        # 10KB
            "static/css/main.css": 15 * 1024,        # 15KB
            "static/css/components-v2.css": 20 * 1024, # 20KB
            "static/css/design-system.css": 15 * 1024, # 15KB
        }
        
        for file_path, max_size in size_limits.items():
            with self.subTest(file=file_path):
                if Path(file_path).exists():
                    actual_size = Path(file_path).stat().st_size
                    self.assertLess(actual_size, max_size,
                                  f"{file_path} too large: {actual_size} bytes > {max_size} bytes")
    
    def test_production_bundle_size(self):
        """Test that production bundle meets size targets"""
        bundle_path = Path("static/build/bundle.min.css")
        
        if bundle_path.exists():
            bundle_size = bundle_path.stat().st_size
            max_bundle_size = 60 * 1024  # 60KB target
            
            self.assertLess(bundle_size, max_bundle_size,
                          f"Bundle too large: {bundle_size} bytes > {max_bundle_size} bytes")
    
    def test_css_syntax_validity(self):
        """Test that CSS files have valid syntax"""
        for css_file in self.css_dir.glob("*.css"):
            with self.subTest(file=str(css_file)):
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic syntax checks
                open_braces = content.count('{')
                close_braces = content.count('}')
                self.assertEqual(open_braces, close_braces,
                               f"Mismatched braces in {css_file}")
                
                # Check for basic CSS structure
                self.assertIn(':', content, f"No CSS properties found in {css_file}")
    
    def test_design_tokens_usage(self):
        """Test that design tokens are properly defined and used"""
        variables_file = Path("static/css/variables.css")
        design_system_file = Path("static/css/design-system.css")
        
        if variables_file.exists():
            with open(variables_file, 'r') as f:
                variables_content = f.read()
            
            # Check for required design tokens
            required_tokens = [
                '--primary-color',
                '--font-family-primary',
                '--spacing-base',
                '--font-size-base'
            ]
            
            for token in required_tokens:
                with self.subTest(token=token):
                    self.assertIn(token, variables_content,
                                f"Required design token missing: {token}")
        
        if design_system_file.exists():
            with open(design_system_file, 'r') as f:
                design_content = f.read()
            
            # Check for semantic color tokens (using actual token names)
            semantic_tokens = [
                '--brand-primary',
                '--surface-primary', 
                '--text-primary',
                '--space-4',
                '--text-base'
            ]
            
            for token in semantic_tokens:
                with self.subTest(token=token):
                    self.assertIn(token, design_content,
                                f"Required semantic token missing: {token}")
    
    def test_accessibility_features(self):
        """Test that accessibility features are implemented"""
        accessibility_file = Path("static/css/accessibility.css")
        
        if accessibility_file.exists():
            with open(accessibility_file, 'r') as f:
                content = f.read()
            
            # Check for required accessibility features
            accessibility_features = [
                'focus-visible',
                'prefers-reduced-motion',
                'prefers-contrast',
                '[aria-'
            ]
            
            for feature in accessibility_features:
                with self.subTest(feature=feature):
                    self.assertIn(feature, content,
                                f"Accessibility feature missing: {feature}")
    
    def test_container_queries(self):
        """Test that container queries are implemented"""
        components_file = Path("static/css/components-v2.css")
        
        if components_file.exists():
            with open(components_file, 'r') as f:
                content = f.read()
            
            # Check for container query features
            container_features = [
                'container-type',
                'container-name',
                '@container'
            ]
            
            for feature in container_features:
                with self.subTest(feature=feature):
                    self.assertIn(feature, content,
                                f"Container query feature missing: {feature}")
    
    def test_css_analyzer_functionality(self):
        """Test that CSS analyzer works correctly"""
        result = subprocess.run(['python', 'analyze_css.py'], 
                              capture_output=True, text=True, timeout=30)
        
        self.assertEqual(result.returncode, 0,
                        f"CSS analyzer failed: {result.stderr}")
        
        # Check that analysis file was created
        analysis_file = Path("css-analysis.json")
        self.assertTrue(analysis_file.exists(),
                       "CSS analysis file not created")
        
        # Verify analysis content
        if analysis_file.exists():
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
            
            # Check for required analysis sections
            required_sections = [
                'file_sizes',
                'css_rules', 
                'custom_properties',
                'accessibility',
                'recommendations'
            ]
            
            for section in required_sections:
                with self.subTest(section=section):
                    self.assertIn(section, analysis_data,
                                f"Analysis section missing: {section}")

class CSSPerformanceTests(unittest.TestCase):
    """Performance-focused CSS tests"""
    
    def test_build_time_performance(self):
        """Test that CSS build completes within reasonable time"""
        start_time = time.time()
        
        result = subprocess.run(['python', 'build_css.py'], 
                              capture_output=True, text=True)
        
        build_time = time.time() - start_time
        max_build_time = 10  # 10 seconds max
        
        self.assertEqual(result.returncode, 0, "Build failed")
        self.assertLess(build_time, max_build_time,
                       f"Build too slow: {build_time:.2f}s > {max_build_time}s")
    
    def test_compression_ratios(self):
        """Test that CSS files achieve good compression ratios"""
        import gzip
        
        for css_file in Path("static/css").glob("*.css"):
            if css_file.is_file():
                with self.subTest(file=str(css_file)):
                    with open(css_file, 'rb') as f:
                        original = f.read()
                    
                    compressed = gzip.compress(original)
                    compression_ratio = (1 - len(compressed) / len(original)) * 100
                    
                    # Expect at least 50% compression for CSS
                    min_compression = 50
                    self.assertGreater(compression_ratio, min_compression,
                                     f"Poor compression in {css_file}: {compression_ratio:.1f}% < {min_compression}%")

def run_css_tests():
    """Run all CSS tests and return results"""
    print("🧪 Running CSS Test Suite for Local Basket...")
    print("="*60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add CSS architecture tests
    test_suite.addTest(unittest.makeSuite(CSSTestFramework))
    test_suite.addTest(unittest.makeSuite(CSSPerformanceTests))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "="*60)
    print("🎯 CSS TEST SUMMARY")
    print("="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print("\n🚨 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    if not result.failures and not result.errors:
        print("\n✅ All CSS tests passed!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_css_tests()
    sys.exit(0 if success else 1)