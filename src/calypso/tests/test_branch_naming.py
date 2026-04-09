"""
Tests for Git branch naming conventions (RULE-10 GitFlow)

Validates that branch names follow the mandatory naming patterns:
- main: Production state (frozen)
- develop: Wild mainline (ad-hoc development)
- stabilization/vX.Y: Scoped backlog + release stabilization (permanent artifact)
- feature/{Timebox}/{IDEA-NNN}-{slug}: Single feature grouped by timebox
- lab/{Timebox}/{slug}: Experimental spike or research
- bugfix/{Timebox}/{Ticket}-{slug}: Planned bug fix
- hotfix/{Ticket}: Emergency production fix
"""

import re
import pytest
from pathlib import Path


# Branch name patterns from RULE-10
BRANCH_PATTERNS = {
    'main': r'^main$',
    'develop': r'^develop$',
    'stabilization': r'^stabilization/v\d+\.\d+$',
    'feature': r'^feature/(\d{4}-Q[1-4]|Sprint-\d+)/IDEA-\d{3}-[a-zA-Z0-9-]+$',
    'lab': r'^lab/(\d{4}-Q[1-4]|Sprint-\d+)/[a-zA-Z0-9-]+$',
    'bugfix': r'^bugfix/(\d{4}-Q[1-4]|Sprint-\d+)/T-\d{3}-[a-zA-Z0-9-]+$',
    'hotfix': r'^hotfix/T-\d{3}-[a-zA-Z0-9-]+$',
}


class TestBranchNaming:
    """Test branch naming convention validation"""
    
    @pytest.mark.parametrize("branch_type,pattern", [
        ("main", BRANCH_PATTERNS['main']),
        ("develop", BRANCH_PATTERNS['develop']),
    ])
    def test_protected_branches(self, branch_type, pattern):
        """Test that protected branches (main, develop) have exact names"""
        assert re.match(pattern, branch_type)
    
    def test_stabilization_pattern(self):
        """Test stabilization/vX.Y pattern"""
        valid_branches = [
            'stabilization/v2.11',
            'stabilization/v1.0',
            'stabilization/v10.15',
        ]
        for branch in valid_branches:
            assert re.match(BRANCH_PATTERNS['stabilization'], branch), f"Failed: {branch}"
        
        invalid_branches = [
            'stabilization/v2',
            'stabilization/v2.11.0',
            'develop-v2.11',
            'release/v2.11',
        ]
        for branch in invalid_branches:
            assert not re.match(BRANCH_PATTERNS['stabilization'], branch), f"Should fail: {branch}"
    
    def test_feature_pattern(self):
        """Test feature/{Timebox}/{IDEA-NNN}-{slug} pattern"""
        valid_branches = [
            'feature/2026-Q2/IDEA-101-authentication',
            'feature/Sprint-42/IDEA-101-authentication',
            'feature/2026-Q1/IDEA-030-critical-gaps',
        ]
        for branch in valid_branches:
            assert re.match(BRANCH_PATTERNS['feature'], branch), f"Failed: {branch}"
        
        invalid_branches = [
            'feature/2026/IDEA-101-authentication',  # Missing quarter
            'feature/Q2/IDEA-101-authentication',     # Missing year
            'feature/2026-Q2/IDEA-1-authentication',  # IDEA number too short
            'feature/2026-Q2/101-authentication',     # Missing IDEA- prefix
            'feature/2026-Q2/T-101-authentication',  # Wrong prefix
        ]
        for branch in invalid_branches:
            assert not re.match(BRANCH_PATTERNS['feature'], branch), f"Should fail: {branch}"
    
    def test_lab_pattern(self):
        """Test lab/{Timebox}/{slug} pattern"""
        valid_branches = [
            'lab/2026-Q2/spike-graphql',
            'lab/Sprint-42/spike-auth',
            'lab/2026-Q1/experiment',
        ]
        for branch in valid_branches:
            assert re.match(BRANCH_PATTERNS['lab'], branch), f"Failed: {branch}"
        
        invalid_branches = [
            'lab/2026/spike-graphql',  # Missing quarter
            'lab/Q2/spike-graphql',    # Missing year
            'lab/2026Q2/spike-graphql',  # Missing hyphen
        ]
        for branch in invalid_branches:
            assert not re.match(BRANCH_PATTERNS['lab'], branch), f"Should fail: {branch}"
    
    def test_bugfix_pattern(self):
        """Test bugfix/{Timebox}/{Ticket}-{slug} pattern"""
        valid_branches = [
            'bugfix/2026-Q2/T-305-UI-Align',
            'bugfix/Sprint-42/T-310-API-Timeout',
        ]
        for branch in valid_branches:
            assert re.match(BRANCH_PATTERNS['bugfix'], branch), f"Failed: {branch}"
        
        invalid_branches = [
            'bugfix/2026-Q2/305-UI-Align',      # Missing T- prefix
            'bugfix/2026-Q2/IDEA-305-UI-Align', # Wrong prefix
            'bugfix/2026-Q2/T-305',             # Missing slug
        ]
        for branch in invalid_branches:
            assert not re.match(BRANCH_PATTERNS['bugfix'], branch), f"Should fail: {branch}"
    
    def test_hotfix_pattern(self):
        """Test hotfix/{Ticket} pattern"""
        valid_branches = [
            'hotfix/T-202-DB-Leak',
            'hotfix/T-101-Critical-Fix',
        ]
        for branch in valid_branches:
            assert re.match(BRANCH_PATTERNS['hotfix'], branch), f"Failed: {branch}"
        
        invalid_branches = [
            'hotfix/202-DB-Leak',         # Missing T- prefix
            'hotfix/T-202',               # Missing slug
            'hotfix/T-0202-DB-Leak',      # Wrong number format (4 digits)
            'bugfix/T-202-DB-Leak',       # Wrong prefix (should be hotfix)
        ]
        for branch in invalid_branches:
            assert not re.match(BRANCH_PATTERNS['hotfix'], branch), f"Should fail: {branch}"


class TestStabilizationBranch:
    """Test stabilization branch requirements per RULE-10"""
    
    def test_stabilization_is_permanent_artifact(self):
        """RULE-10: stabilization/vX.Y is a permanent artifact, never deleted"""
        # This is a documentation test - verifying the pattern exists
        # and the permanence requirement is understood
        pattern = BRANCH_PATTERNS['stabilization']
        branch = 'stabilization/v2.16'
        assert re.match(pattern, branch)
    
    def test_stabilization_contains_version(self):
        """RULE-10: stabilization branch must contain semantic version"""
        pattern = BRANCH_PATTERNS['stabilization']
        
        # Must have v followed by major.minor
        assert re.match(pattern, 'stabilization/v2.16')
        assert re.match(pattern, 'stabilization/v10.0')
        assert re.match(pattern, 'stabilization/v1.1')
        
        # Should not have patch version
        assert not re.match(pattern, 'stabilization/v2.16.0')
        assert not re.match(pattern, 'stabilization/v2.16.1')


class TestFeatureBranch:
    """Test feature branch requirements per RULE-10"""
    
    def test_feature_requires_timebox(self):
        """RULE-10: feature branches must have a timebox (Quarter or Sprint)"""
        pattern = BRANCH_PATTERNS['feature']
        
        # Quarter-based timebox
        assert re.match(pattern, 'feature/2026-Q2/IDEA-001-test')
        
        # Sprint-based timebox
        assert re.match(pattern, 'feature/Sprint-42/IDEA-001-test')
        
        # Without timebox should fail
        assert not re.match(pattern, 'feature/IDEA-001-test')
    
    def test_feature_requires_idea_prefix(self):
        """RULE-10: feature branches must have IDEA-NNN prefix"""
        pattern = BRANCH_PATTERNS['feature']
        
        # Correct format
        assert re.match(pattern, 'feature/2026-Q2/IDEA-101-authentication')
        
        # Wrong prefixes should fail
        assert not re.match(pattern, 'feature/2026-Q2/T-101-authentication')
        assert not re.match(pattern, 'feature/2026-Q2/BUG-101-authentication')
        assert not re.match(pattern, 'feature/2026-Q2/101-authentication')
