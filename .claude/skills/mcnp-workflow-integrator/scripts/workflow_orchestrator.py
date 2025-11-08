"""
MCNP Multi-Physics Workflow Orchestrator

Automates execution of multi-stage reactor analysis workflows.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class WorkflowStage:
    """Base class for workflow stages."""

    def __init__(self, name: str, working_dir: Path):
        self.name = name
        self.working_dir = Path(working_dir)
        self.status = 'pending'
        self.start_time = None
        self.end_time = None
        self.error_msg = None

    def execute(self) -> bool:
        """
        Execute this stage.

        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate prerequisites for this stage.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        return True, []

    def run(self) -> bool:
        """
        Run this stage with validation and error handling.

        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"STAGE: {self.name}")
        print(f"{'='*60}")

        # Validate prerequisites
        print(f"Validating prerequisites...")
        is_valid, issues = self.validate()
        if not is_valid:
            print(f"❌ Validation failed:")
            for issue in issues:
                print(f"   - {issue}")
            self.status = 'validation_failed'
            self.error_msg = '; '.join(issues)
            return False
        print(f"✓ Validation passed")

        # Execute stage
        print(f"Executing {self.name}...")
        self.status = 'running'
        self.start_time = time.time()

        try:
            success = self.execute()
            self.end_time = time.time()

            if success:
                self.status = 'completed'
                elapsed = self.end_time - self.start_time
                print(f"✓ {self.name} completed in {elapsed:.1f} seconds")
                return True
            else:
                self.status = 'failed'
                print(f"❌ {self.name} failed")
                return False

        except Exception as e:
            self.end_time = time.time()
            self.status = 'error'
            self.error_msg = str(e)
            print(f"❌ {self.name} error: {e}")
            return False


class InputGenerationStage(WorkflowStage):
    """Generate MCNP inputs from scripts."""

    def __init__(self, working_dir: Path, script: str, **kwargs):
        super().__init__("Input Generation", working_dir)
        self.script = script
        self.kwargs = kwargs

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        # Check script exists
        script_path = self.working_dir / self.script
        if not script_path.exists():
            issues.append(f"Generation script not found: {script_path}")

        # Check Python available
        try:
            subprocess.run(['python', '--version'],
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            issues.append("Python not available")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        cmd = ['python', self.script]
        result = subprocess.run(cmd, cwd=self.working_dir,
                              capture_output=True, text=True)

        if result.returncode != 0:
            self.error_msg = result.stderr
            print(result.stderr)
            return False

        print(result.stdout)
        return True


class ValidationStage(WorkflowStage):
    """Validate generated inputs."""

    def __init__(self, working_dir: Path, input_files: List[Path]):
        super().__init__("Input Validation", working_dir)
        self.input_files = [Path(f) for f in input_files]

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        for inp in self.input_files:
            if not inp.exists():
                issues.append(f"Input file not found: {inp}")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        # Import validation functions
        sys.path.insert(0, str(self.working_dir / 'scripts'))
        try:
            from validate import validate_mcnp_input
        except ImportError:
            print("Warning: validate.py not found, skipping detailed checks")
            return True

        all_valid = True
        for inp in self.input_files:
            print(f"  Validating {inp.name}...")
            result = validate_mcnp_input(inp)

            if not result['valid']:
                all_valid = False
                print(f"    ❌ Issues found:")
                for issue in result['issues']:
                    print(f"       - {issue}")
            else:
                print(f"    ✓ Valid")

        return all_valid


class MCNPExecutionStage(WorkflowStage):
    """Execute MCNP calculations."""

    def __init__(self, working_dir: Path, input_files: List[Path],
                 mcnp_cmd: str = 'mcnp6', tasks: int = 1):
        super().__init__("MCNP Execution", working_dir)
        self.input_files = [Path(f) for f in input_files]
        self.mcnp_cmd = mcnp_cmd
        self.tasks = tasks

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        # Check MCNP available
        try:
            result = subprocess.run([self.mcnp_cmd, 'v'],
                                  capture_output=True, timeout=5)
            # MCNP prints version to stderr typically
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            issues.append(f"MCNP not available (command: {self.mcnp_cmd})")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        for inp in self.input_files:
            print(f"  Running {inp.name}...")

            # MCNP command: mcnp6 i=input.i n=input.
            output_prefix = inp.stem + '.'
            cmd = [self.mcnp_cmd, f'i={inp}', f'n={output_prefix}',
                   f'tasks {self.tasks}']

            # Run MCNP
            result = subprocess.run(cmd, cwd=inp.parent,
                                  capture_output=True, text=True)

            if result.returncode != 0:
                print(f"    ❌ MCNP failed")
                print(result.stderr)
                self.error_msg = f"MCNP failed for {inp.name}"
                return False

            # Check for fatal errors in output
            output_file = inp.parent / (output_prefix + 'o')
            if output_file.exists():
                with open(output_file, 'r') as f:
                    content = f.read()
                    if 'fatal error' in content.lower():
                        print(f"    ❌ Fatal error in MCNP output")
                        self.error_msg = f"Fatal error in {inp.name}"
                        return False

            print(f"    ✓ Completed")

        return True


class PostProcessingStage(WorkflowStage):
    """Post-process results."""

    def __init__(self, working_dir: Path, script: str):
        super().__init__("Post-Processing", working_dir)
        self.script = script

    def validate(self) -> Tuple[bool, List[str]]:
        issues = []

        script_path = self.working_dir / self.script
        if not script_path.exists():
            issues.append(f"Post-processing script not found: {script_path}")

        return len(issues) == 0, issues

    def execute(self) -> bool:
        cmd = ['python', self.script]
        result = subprocess.run(cmd, cwd=self.working_dir,
                              capture_output=True, text=True)

        if result.returncode != 0:
            self.error_msg = result.stderr
            print(result.stderr)
            return False

        print(result.stdout)
        return True


class Workflow:
    """Complete multi-stage workflow."""

    def __init__(self, name: str, working_dir: Path):
        self.name = name
        self.working_dir = Path(working_dir)
        self.stages: List[WorkflowStage] = []
        self.current_stage = 0

    def add_stage(self, stage: WorkflowStage):
        """Add a stage to the workflow."""
        self.stages.append(stage)

    def run(self, start_from: int = 0) -> bool:
        """
        Execute the complete workflow.

        Args:
            start_from: Stage index to start from (for restart)

        Returns:
            True if all stages successful, False otherwise
        """
        print(f"\n{'#'*60}")
        print(f"# WORKFLOW: {self.name}")
        print(f"# Stages: {len(self.stages)}")
        print(f"# Working Directory: {self.working_dir}")
        print(f"{'#'*60}")

        for i, stage in enumerate(self.stages[start_from:], start=start_from):
            self.current_stage = i

            success = stage.run()

            if not success:
                print(f"\n❌ Workflow failed at stage {i+1}/{len(self.stages)}: {stage.name}")
                self._print_summary()
                return False

        print(f"\n{'='*60}")
        print(f"✓ Workflow completed successfully")
        print(f"{'='*60}")
        self._print_summary()
        return True

    def _print_summary(self):
        """Print workflow execution summary."""
        print(f"\nWorkflow Summary:")
        print(f"{'Stage':<30} {'Status':<15} {'Time (s)':<10}")
        print(f"{'-'*60}")

        for i, stage in enumerate(self.stages):
            elapsed = ''
            if stage.start_time and stage.end_time:
                elapsed = f"{stage.end_time - stage.start_time:.1f}"

            status_symbol = {
                'pending': '⏸',
                'running': '▶',
                'completed': '✓',
                'failed': '❌',
                'error': '💥',
                'validation_failed': '⚠'
            }.get(stage.status, '?')

            print(f"{i+1}. {stage.name:<27} {status_symbol} {stage.status:<13} {elapsed:<10}")

            if stage.error_msg:
                print(f"   Error: {stage.error_msg}")


# Example usage
if __name__ == "__main__":
    # Define workflow
    workflow = Workflow("HTGR Burnup-to-SDR Analysis", Path.cwd())

    # Stage 1: Generate inputs
    workflow.add_stage(
        InputGenerationStage(
            working_dir=Path.cwd(),
            script='scripts/create_inputs.py'
        )
    )

    # Stage 2: Validate inputs
    workflow.add_stage(
        ValidationStage(
            working_dir=Path.cwd(),
            input_files=[
                Path('inputs/bench_138B.i'),
                Path('inputs/bench_139A.i'),
                # ... etc
            ]
        )
    )

    # Stage 3: Run MCNP
    workflow.add_stage(
        MCNPExecutionStage(
            working_dir=Path.cwd(),
            input_files=[Path('inputs/bench_138B.i')],
            mcnp_cmd='mcnp6',
            tasks=8
        )
    )

    # Stage 4: Post-process
    workflow.add_stage(
        PostProcessingStage(
            working_dir=Path.cwd(),
            script='scripts/post_process.py'
        )
    )

    # Run workflow
    success = workflow.run()
    sys.exit(0 if success else 1)
