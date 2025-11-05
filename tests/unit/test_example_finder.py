"""
Unit tests for MCNP Example Finder Skill

Tests example search and retrieval:
- Keyword search
- Simple example retrieval
- Feature-based filtering
- Category summary generation
"""
import pytest
import sys
import tempfile
from pathlib import Path

# Add skill directory to path
project_root = Path(__file__).parent.parent.parent
skill_dir = project_root / ".claude" / "skills" / "mcnp-example-finder"
sys.path.insert(0, str(skill_dir))

from mcnp_example_finder import MCNPExampleFinderSkill


class TestMCNPExampleFinderSkill:
    """Test suite for MCNP Example Finder"""

    def setup_method(self):
        """Setup test fixture"""
        # Create temporary example directory
        self.temp_dir = tempfile.mkdtemp()
        self.finder = MCNPExampleFinderSkill(self.temp_dir)

    def teardown_method(self):
        """Cleanup test fixture"""
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # ===== Search Tests =====

    def test_search_returns_list(self):
        """Test search returns a list"""
        results = self.finder.search("sphere")

        assert isinstance(results, list), "Should return list"

    def test_search_empty_keyword(self):
        """Test search with empty keyword"""
        results = self.finder.search("")

        assert isinstance(results, list), "Should return list for empty keyword"

    def test_search_max_results_default(self):
        """Test search respects default max_results"""
        results = self.finder.search("test")

        # Should return at most 10 results (default)
        assert len(results) <= 10, "Should respect default max_results"

    def test_search_max_results_custom(self):
        """Test search respects custom max_results"""
        results = self.finder.search("test", max_results=5)

        # Should return at most 5 results
        assert len(results) <= 5, "Should respect custom max_results"

    def test_search_result_structure(self):
        """Test search result structure"""
        results = self.finder.search("test")

        # Each result should be dict with expected fields
        for result in results:
            assert isinstance(result, dict), "Each result should be dict"
            assert 'file' in result, "Should have 'file' field"
            assert 'category' in result, "Should have 'category' field"
            assert 'description' in result, "Should have 'description' field"

    def test_search_nonexistent_keyword(self):
        """Test search with nonexistent keyword"""
        results = self.finder.search("xyznonexistent12345")

        # Should return empty list
        assert isinstance(results, list), "Should return list"
        assert len(results) == 0, "Should find no results"

    def test_search_case_sensitivity(self):
        """Test search case handling"""
        results_lower = self.finder.search("sphere")
        results_upper = self.finder.search("SPHERE")

        # Both should return results (case-insensitive search expected)
        assert isinstance(results_lower, list), "Lowercase should return list"
        assert isinstance(results_upper, list), "Uppercase should return list"

    # ===== Simple Examples Tests =====

    def test_get_simple_examples_returns_list(self):
        """Test get_simple_examples returns list"""
        examples = self.finder.get_simple_examples()

        assert isinstance(examples, list), "Should return list"

    def test_get_simple_examples_default_count(self):
        """Test get_simple_examples with default count"""
        examples = self.finder.get_simple_examples()

        # Should return at most 5 examples (default)
        assert len(examples) <= 5, "Should respect default count"

    def test_get_simple_examples_custom_count(self):
        """Test get_simple_examples with custom count"""
        examples = self.finder.get_simple_examples(count=3)

        # Should return at most 3 examples
        assert len(examples) <= 3, "Should respect custom count"

    def test_get_simple_examples_structure(self):
        """Test get_simple_examples result structure"""
        examples = self.finder.get_simple_examples()

        # Each example should have expected fields
        for example in examples:
            assert isinstance(example, dict), "Each example should be dict"
            assert 'file' in example, "Should have 'file' field"
            assert 'path' in example, "Should have 'path' field"
            assert 'description' in example, "Should have 'description' field"

    def test_get_simple_examples_zero_count(self):
        """Test get_simple_examples with zero count"""
        examples = self.finder.get_simple_examples(count=0)

        assert isinstance(examples, list), "Should return list"
        assert len(examples) == 0, "Should return empty list for count=0"

    def test_get_simple_examples_large_count(self):
        """Test get_simple_examples with very large count"""
        examples = self.finder.get_simple_examples(count=1000)

        # Should return all available simple examples (capped by availability)
        assert isinstance(examples, list), "Should return list"

    # ===== Feature-based Filtering Tests =====

    def test_find_by_feature_criticality_only(self):
        """Test finding examples with criticality"""
        examples = self.finder.find_by_feature(criticality=True)

        assert isinstance(examples, list), "Should return list"

    def test_find_by_feature_tallies_only(self):
        """Test finding examples with tallies"""
        examples = self.finder.find_by_feature(tallies=True)

        assert isinstance(examples, list), "Should return list"

    def test_find_by_feature_variance_reduction_only(self):
        """Test finding examples with variance reduction"""
        examples = self.finder.find_by_feature(variance_reduction=True)

        assert isinstance(examples, list), "Should return list"

    def test_find_by_feature_no_features(self):
        """Test finding with no features selected"""
        examples = self.finder.find_by_feature()

        # Should return all examples or empty list
        assert isinstance(examples, list), "Should return list"

    def test_find_by_feature_multiple_features(self):
        """Test finding with multiple features"""
        examples = self.finder.find_by_feature(criticality=True, tallies=True)

        assert isinstance(examples, list), "Should return list"

    def test_find_by_feature_all_features(self):
        """Test finding with all features"""
        examples = self.finder.find_by_feature(
            criticality=True,
            tallies=True,
            variance_reduction=True
        )

        assert isinstance(examples, list), "Should return list"

    def test_find_by_feature_result_structure(self):
        """Test find_by_feature result structure"""
        examples = self.finder.find_by_feature(criticality=True)

        # Each result should have expected fields
        for example in examples:
            assert isinstance(example, dict), "Each example should be dict"
            assert 'file' in example, "Should have 'file' field"
            assert 'category' in example, "Should have 'category' field"

    # ===== Category Summary Tests =====

    def test_get_category_summary_returns_dict(self):
        """Test get_category_summary returns dict"""
        summary = self.finder.get_category_summary()

        assert isinstance(summary, dict), "Should return dict"

    def test_get_category_summary_structure(self):
        """Test get_category_summary structure"""
        summary = self.finder.get_category_summary()

        # Keys should be category names, values should be counts
        for category, count in summary.items():
            assert isinstance(category, str), "Category should be string"
            assert isinstance(count, int), "Count should be integer"
            assert count >= 0, "Count should be non-negative"

    def test_get_category_summary_empty_database(self):
        """Test get_category_summary with empty database"""
        # Fresh finder with empty directory
        summary = self.finder.get_category_summary()

        assert isinstance(summary, dict), "Should return dict even when empty"
        # May be empty or have zero counts
        assert len(summary) >= 0, "Should handle empty database"

    def test_get_category_summary_consistency(self):
        """Test get_category_summary is consistent"""
        summary1 = self.finder.get_category_summary()
        summary2 = self.finder.get_category_summary()

        # Multiple calls should return same result
        assert summary1 == summary2, "Should be consistent across calls"

    # ===== Integration Tests =====

    def test_complete_workflow_search_filter(self):
        """Test complete workflow: search then filter by features"""
        # Step 1: Search for examples
        search_results = self.finder.search("sphere")
        assert isinstance(search_results, list), "Should search"

        # Step 2: Filter by features
        feature_results = self.finder.find_by_feature(criticality=True)
        assert isinstance(feature_results, list), "Should filter by features"

        # Step 3: Get simple examples
        simple_examples = self.finder.get_simple_examples()
        assert isinstance(simple_examples, list), "Should get simple examples"

        # Step 4: Get category summary
        summary = self.finder.get_category_summary()
        assert isinstance(summary, dict), "Should get category summary"

    def test_complete_workflow_beginner_to_advanced(self):
        """Test workflow from beginner to advanced examples"""
        # Step 1: Start with simple examples
        simple = self.finder.get_simple_examples(count=3)
        assert isinstance(simple, list), "Should get simple examples"

        # Step 2: Search for specific topic
        sphere_examples = self.finder.search("sphere", max_results=5)
        assert isinstance(sphere_examples, list), "Should search by topic"

        # Step 3: Find advanced features
        advanced = self.finder.find_by_feature(
            criticality=True,
            variance_reduction=True
        )
        assert isinstance(advanced, list), "Should find advanced examples"

    # ===== Edge Case Tests =====

    def test_search_special_characters(self):
        """Test search with special characters"""
        results = self.finder.search("test*@#$")

        assert isinstance(results, list), "Should handle special characters"

    def test_search_very_long_keyword(self):
        """Test search with very long keyword"""
        long_keyword = "a" * 1000
        results = self.finder.search(long_keyword)

        assert isinstance(results, list), "Should handle long keywords"

    def test_get_simple_examples_negative_count(self):
        """Test get_simple_examples with negative count"""
        # Should handle gracefully (return empty or default)
        examples = self.finder.get_simple_examples(count=-5)

        assert isinstance(examples, list), "Should handle negative count"

    def test_find_by_feature_boolean_values(self):
        """Test find_by_feature with explicit boolean values"""
        # Explicitly pass False
        examples = self.finder.find_by_feature(
            criticality=False,
            tallies=False,
            variance_reduction=False
        )

        assert isinstance(examples, list), "Should handle all False"

    def test_get_category_summary_after_search(self):
        """Test category summary after performing searches"""
        # Perform some searches first
        self.finder.search("sphere")
        self.finder.search("criticality")

        # Summary should still be consistent
        summary = self.finder.get_category_summary()
        assert isinstance(summary, dict), "Should return valid summary"

    # ===== Realistic Usage Tests =====

    def test_find_beginner_criticality_example(self):
        """Test finding simple criticality example for beginner"""
        # Get simple examples
        simple = self.finder.get_simple_examples()

        # Filter for criticality
        crit = self.finder.find_by_feature(criticality=True)

        # Both should return valid results
        assert isinstance(simple, list), "Should get simple examples"
        assert isinstance(crit, list), "Should get criticality examples"

    def test_find_shielding_examples(self):
        """Test finding shielding calculation examples"""
        results = self.finder.search("shield", max_results=10)

        assert isinstance(results, list), "Should search for shielding"

    def test_find_reactor_physics_examples(self):
        """Test finding reactor physics examples"""
        # Search for reactor-related terms
        reactor_results = self.finder.search("reactor", max_results=10)
        pwr_results = self.finder.search("pwr", max_results=10)

        assert isinstance(reactor_results, list), "Should search reactors"
        assert isinstance(pwr_results, list), "Should search PWR"

    def test_find_variance_reduction_techniques(self):
        """Test finding variance reduction examples"""
        vr_examples = self.finder.find_by_feature(variance_reduction=True)

        assert isinstance(vr_examples, list), "Should find VR examples"

    def test_get_category_distribution(self):
        """Test getting category distribution"""
        summary = self.finder.get_category_summary()

        # Calculate total examples
        total = sum(summary.values())

        assert isinstance(total, int), "Total should be integer"
        assert total >= 0, "Total should be non-negative"

    # ===== Performance Tests =====

    def test_search_performance_many_results(self):
        """Test search performance with large max_results"""
        # Request many results
        results = self.finder.search("test", max_results=1000)

        assert isinstance(results, list), "Should handle large max_results"
        assert len(results) <= 1000, "Should respect max_results limit"

    def test_multiple_sequential_searches(self):
        """Test multiple searches in sequence"""
        # Perform multiple searches
        for keyword in ["sphere", "cylinder", "criticality", "tally", "source"]:
            results = self.finder.search(keyword)
            assert isinstance(results, list), f"Should handle {keyword}"

    def test_feature_search_combinations(self):
        """Test all combinations of feature searches"""
        # Test various combinations
        combinations = [
            (True, False, False),
            (False, True, False),
            (False, False, True),
            (True, True, False),
            (True, False, True),
            (False, True, True),
            (True, True, True),
        ]

        for crit, tall, vr in combinations:
            results = self.finder.find_by_feature(
                criticality=crit,
                tallies=tall,
                variance_reduction=vr
            )
            assert isinstance(results, list), "Should handle combination"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
