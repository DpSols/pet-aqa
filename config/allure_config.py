import json
import os
import platform
from dataclasses import dataclass, field
from pathlib import Path

from config.settings import Settings


@dataclass(frozen=True)
class FailureCategory:
    name: str
    matched_statuses: list[str]
    message_regex: str = ".*"


@dataclass(frozen=True)
class AllureConfig:
    results_dir: str = "allure-results"
    report_title: str = "Pet Automation Test Report"
    categories: list[FailureCategory] = field(
        default_factory=lambda: [
            FailureCategory("Product defects", ["failed"], r".*AssertionError.*"),
            FailureCategory("Test defects", ["broken"], r".*"),
            FailureCategory("Infrastructure failures", ["broken"], r".*(ConnectionError|TimeoutError).*"),
        ]
    )

    def write_all(self, settings: Settings) -> None:
        results_path = Path(self.results_dir)
        results_path.mkdir(parents=True, exist_ok=True)

        self._write_environment(settings, results_path)
        self._write_categories(results_path)
        self._write_executor(results_path)

    def _write_environment(self, settings: Settings, results_path: Path) -> None:
        env_props = {
            "api.base_url": settings.api.base_url,
            "web.base_url": settings.web.base_url,
            "web.headless": str(settings.web.headless),
            "python.version": platform.python_version(),
            "platform.system": platform.system(),
            "platform.release": platform.release(),
        }

        props_content = "\n".join(f"{k}={v}" for k, v in env_props.items())
        (results_path / "environment.properties").write_text(props_content)

    def _write_categories(self, results_path: Path) -> None:
        categories_list = []
        for cat in self.categories:
            categories_list.append(
                {
                    "name": cat.name,
                    "matchedStatuses": cat.matched_statuses,
                    "messageRegex": cat.message_regex,
                }
            )

        (results_path / "categories.json").write_text(json.dumps(categories_list, indent=2))

    def _write_executor(self, results_path: Path) -> None:
        executor_type = "local"
        build_name = "Local Test Run"
        build_url = None

        if os.getenv("CI"):
            executor_type = "gitlab"
            build_name = os.getenv("CI_JOB_NAME", "GitLab CI Job")
            build_url = os.getenv("CI_JOB_URL", "")

        executor = {
            "name": executor_type,
            "type": executor_type,
            "buildName": build_name,
        }
        if build_url:
            executor["buildUrl"] = build_url

        (results_path / "executor.json").write_text(json.dumps(executor, indent=2))
