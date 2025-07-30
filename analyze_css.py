#!/usr/bin/env python3
"""
CSS Bundle Analyzer for Local Basket
Analyzes CSS usage, performance metrics, and provides optimization recommendations
"""

import os
import re
import gzip
import json
from pathlib import Path
from collections import defaultdict
import subprocess
import sys

class CSSAnalyzer:
    def __init__(self, css_dir="static/css", build_dir="static/build"):
        self.css_dir = Path(css_dir)
        self.build_dir = Path(build_dir)
        self.stats = defaultdict(dict)
        
    def analyze_file_sizes(self):
        """Analyze file sizes and compression ratios"""
        print("📊 Analyzing CSS file sizes and compression...")
        
        for css_file in self.css_dir.glob("**/*.css"):
            if css_file.is_file() and not str(css_file).startswith('static/build'):
                size = css_file.stat().st_size
                
                # Try to compress for analysis
                with open(css_file, 'rb') as f:
                    content = f.read()
                    compressed = gzip.compress(content)
                    compression_ratio = (1 - len(compressed) / len(content)) * 100
                
                self.stats['file_sizes'][str(css_file)] = {
                    'size': size,
                    'size_kb': round(size / 1024, 2),
                    'compressed_size': len(compressed),
                    'compressed_kb': round(len(compressed) / 1024, 2),
                    'compression_ratio': round(compression_ratio, 1)
                }
        
        # Analyze build files
        if self.build_dir.exists():
            for build_file in self.build_dir.glob("*.css"):
                size = build_file.stat().st_size
                self.stats['build_files'][str(build_file)] = {
                    'size': size,
                    'size_kb': round(size / 1024, 2)
                }
    
    def analyze_css_rules(self):
        """Analyze CSS rules, selectors, and properties"""
        print("🔍 Analyzing CSS rules and selectors...")
        
        total_rules = 0
        total_selectors = 0
        property_usage = defaultdict(int)
        selector_patterns = defaultdict(int)
        
        for css_file in self.css_dir.glob("**/*.css"):
            if css_file.is_file() and not str(css_file).startswith('static/build'):
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Count rules (basic regex)
                rules = re.findall(r'{[^}]*}', content)
                total_rules += len(rules)
                
                # Count selectors
                selectors = re.findall(r'([^{]+){', content)
                total_selectors += len(selectors)
                
                # Analyze selector patterns
                for selector in selectors:
                    selector = selector.strip()
                    if selector.startswith('.'):
                        selector_patterns['class'] += 1
                    elif selector.startswith('#'):
                        selector_patterns['id'] += 1
                    elif selector.startswith('@'):
                        selector_patterns['at-rule'] += 1
                    else:
                        selector_patterns['element'] += 1
                
                # Count property usage
                properties = re.findall(r'([a-z-]+):', content)
                for prop in properties:
                    if prop not in ['http', 'https']:  # Filter out URLs
                        property_usage[prop] += 1
        
        self.stats['css_rules'] = {
            'total_rules': total_rules,
            'total_selectors': total_selectors,
            'selector_patterns': dict(selector_patterns),
            'most_used_properties': dict(sorted(property_usage.items(), 
                                               key=lambda x: x[1], reverse=True)[:10])
        }
    
    def analyze_custom_properties(self):
        """Analyze CSS custom properties (variables) usage"""
        print("🎨 Analyzing CSS custom properties...")
        
        custom_props = defaultdict(int)
        custom_prop_definitions = set()
        
        for css_file in self.css_dir.glob("**/*.css"):
            if css_file.is_file() and not str(css_file).startswith('static/build'):
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find custom property definitions
                definitions = re.findall(r'--([a-z0-9-]+):', content)
                custom_prop_definitions.update(definitions)
                
                # Find custom property usage
                usage = re.findall(r'var\(--([a-z0-9-]+)\)', content)
                for prop in usage:
                    custom_props[prop] += 1
        
        self.stats['custom_properties'] = {
            'total_defined': len(custom_prop_definitions),
            'total_usage': sum(custom_props.values()),
            'most_used': dict(sorted(custom_props.items(), 
                                   key=lambda x: x[1], reverse=True)[:10]),
            'unused_definitions': list(set(custom_prop_definitions) - set(custom_props.keys()))
        }
    
    def check_accessibility_features(self):
        """Check for accessibility-related CSS features"""
        print("♿ Analyzing accessibility features...")
        
        accessibility_features = {
            'focus_styles': 0,
            'reduced_motion': 0,
            'high_contrast': 0,
            'aria_selectors': 0,
            'skip_links': 0
        }
        
        for css_file in self.css_dir.glob("**/*.css"):
            if css_file.is_file() and not str(css_file).startswith('static/build'):
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if ':focus' in content or 'focus-visible' in content:
                        accessibility_features['focus_styles'] += content.count(':focus')
                    
                    if 'prefers-reduced-motion' in content:
                        accessibility_features['reduced_motion'] += 1
                    
                    if 'prefers-contrast' in content or 'forced-colors' in content:
                        accessibility_features['high_contrast'] += 1
                    
                    if '[aria-' in content:
                        accessibility_features['aria_selectors'] += content.count('[aria-')
                    
                    if 'skip' in content.lower():
                        accessibility_features['skip_links'] += 1
        
        self.stats['accessibility'] = accessibility_features
    
    def generate_recommendations(self):
        """Generate optimization recommendations"""
        print("💡 Generating optimization recommendations...")
        
        recommendations = []
        
        # File size recommendations
        for file_path, data in self.stats.get('file_sizes', {}).items():
            if data['size_kb'] > 50:
                recommendations.append(f"⚠️  {file_path} is {data['size_kb']}KB - consider splitting or optimizing")
            
            if data['compression_ratio'] < 60:
                recommendations.append(f"📦 {file_path} has low compression ratio ({data['compression_ratio']}%) - check for repetitive code")
        
        # Custom properties recommendations
        unused_props = self.stats.get('custom_properties', {}).get('unused_definitions', [])
        if unused_props:
            recommendations.append(f"🗑️  Found {len(unused_props)} unused CSS custom properties - consider removing: {', '.join(unused_props[:5])}")
        
        # Accessibility recommendations
        accessibility = self.stats.get('accessibility', {})
        if accessibility.get('focus_styles', 0) < 5:
            recommendations.append("♿ Consider adding more focus styles for better keyboard navigation")
        
        if accessibility.get('reduced_motion', 0) == 0:
            recommendations.append("♿ Add prefers-reduced-motion media queries for accessibility")
        
        self.stats['recommendations'] = recommendations
    
    def print_report(self):
        """Print comprehensive analysis report"""
        print("\n" + "="*80)
        print("🎯 LOCAL BASKET CSS ANALYSIS REPORT")
        print("="*80)
        
        # File sizes
        print("\n📊 FILE SIZE ANALYSIS:")
        total_size = 0
        total_compressed = 0
        
        for file_path, data in self.stats.get('file_sizes', {}).items():
            print(f"   {Path(file_path).name:<25} {data['size_kb']:>8}KB → {data['compressed_kb']:>6}KB ({data['compression_ratio']:>5}%)")
            total_size += data['size']
            total_compressed += data['compressed_size']
        
        if total_size > 0:
            overall_compression = (1 - total_compressed / total_size) * 100
            print(f"   {'TOTAL':<25} {total_size/1024:>8.1f}KB → {total_compressed/1024:>6.1f}KB ({overall_compression:>5.1f}%)")
        
        # Build files
        if 'build_files' in self.stats:
            print("\n🏗️  BUILD FILE SIZES:")
            for file_path, data in self.stats['build_files'].items():
                print(f"   {Path(file_path).name:<25} {data['size_kb']:>8}KB")
        
        # CSS rules
        if 'css_rules' in self.stats:
            rules = self.stats['css_rules']
            print(f"\n🔍 CSS RULES ANALYSIS:")
            print(f"   Total Rules:      {rules['total_rules']}")
            print(f"   Total Selectors:  {rules['total_selectors']}")
            print(f"   Selector Types:   {rules['selector_patterns']}")
            print(f"   Top Properties:   {list(rules['most_used_properties'].keys())[:5]}")
        
        # Custom properties
        if 'custom_properties' in self.stats:
            props = self.stats['custom_properties']
            print(f"\n🎨 CSS CUSTOM PROPERTIES:")
            print(f"   Defined:          {props['total_defined']}")
            print(f"   Total Usage:      {props['total_usage']}")
            print(f"   Most Used:        {list(props['most_used'].keys())[:3]}")
            if props['unused_definitions']:
                print(f"   Unused:           {len(props['unused_definitions'])} variables")
        
        # Accessibility
        if 'accessibility' in self.stats:
            a11y = self.stats['accessibility']
            print(f"\n♿ ACCESSIBILITY FEATURES:")
            print(f"   Focus Styles:     {a11y['focus_styles']}")
            print(f"   Reduced Motion:   {'✅' if a11y['reduced_motion'] > 0 else '❌'}")
            print(f"   High Contrast:    {'✅' if a11y['high_contrast'] > 0 else '❌'}")
            print(f"   ARIA Selectors:   {a11y['aria_selectors']}")
        
        # Recommendations
        if 'recommendations' in self.stats:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in self.stats['recommendations']:
                print(f"   {rec}")
        
        print("\n" + "="*80)
    
    def export_json(self, filename="css-analysis.json"):
        """Export analysis results to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"📋 Analysis exported to {filename}")

def main():
    """Main execution function"""
    print("🔬 Starting CSS Analysis for Local Basket...")
    
    analyzer = CSSAnalyzer()
    
    try:
        analyzer.analyze_file_sizes()
        analyzer.analyze_css_rules()
        analyzer.analyze_custom_properties()
        analyzer.check_accessibility_features()
        analyzer.generate_recommendations()
        analyzer.print_report()
        analyzer.export_json()
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()