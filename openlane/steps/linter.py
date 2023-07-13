# Copyright 2023 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import re
import sys

from typing import List, Optional, Tuple

from .step import Step, ViewsUpdate, MetricsUpdate, StepError

from ..config import Variable
from ..state import State, Path


@Step.factory.register()
class Lint(Step):
    """ """

    id = "Linter.Lint"
    inputs = []  # The input RTL is part of the configuration
    outputs = []
    flow_control_variable = "RUN_LINTER"
    config_vars = [
        Variable(
            "VERILOG_FILES",
            List[Path],
            "The paths of the design's Verilog files.",
        ),
        Variable(
            "RUN_LINTER",
            bool,
            "Enables/disables this step.",
            default=True,
            deprecated_names=["RUN_VERILATOR"],
        ),
        Variable(
            "LINTER_INCLUDE_PDK_MODELS",
            bool,
            "Include verilog models of the PDK",
            default=False,
        ),
        Variable(
            "LINTER_RELATIVE_INCLUDES",
            bool,
            "When a file references an include file, resolve the filename relative to the path of the referencing file, instead of relative to the current directory.",
            default=True,
            deprecated_names=["VERILATOR_REALTIVE_INCLUDES"],
        ),
        Variable(
            "SYNTH_DEFINES",
            Optional[List[str]],
            "Synthesis defines",
        ),
        Variable(
            "LINTER_DEFINES",
            Optional[List[str]],
            "Linter defines overriding SYNTH_DEFINES",
        ),
        Variable(
            "QUIT_ON_LINTER_WARNINGS",
            bool,
            "Quit on linter warnings.",
            default=False,
            deprecated_names=["QUIT_ON_VERILATOR_WARNINGS"],
        ),
    ]

    def run(self, state_in: State, **kwargs) -> Tuple[ViewsUpdate, MetricsUpdate]:
        kwargs, env = self.extract_env(kwargs)
        views_updates: ViewsUpdate = {}
        metrics_updates: MetricsUpdate = {}
        extra_args = []

        if not self.config["QUIT_ON_LINTER_WARNINGS"]:
            extra_args.append("--Wno-fatal")

        if self.config["LINTER_RELATIVE_INCLUDES"]:
            extra_args.append("--relative-includes")

        defines = []
        if self.config["LINTER_DEFINES"]:
            for define in self.config["LINTER_DEFINES"]:
                defines.append(f"+define+{define}")
        elif self.config["SYNTH_DEFINES"]:
            for define in self.config["SYNTH_DEFINES"]:
                defines.append(f"+define+{define}")
        extra_args += defines

        clean_exit = True
        try:
            self.run_subprocess(
                [
                    "verilator",
                    "--lint-only",
                    "--Wall",
                    "--Wno-DECLFILENAME",
                    "--top-module",
                    self.config["DESIGN_NAME"],
                ]
                + self.config["VERILOG_FILES"]
                + extra_args,
                env=env,
            )
        except:
            clean_exit = False

        warnings_count = 0
        errors_count = 0
        timing_constructs = 0

        error_pattern = re.compile(r"\s*\%Error: Exiting due to (\d+) error\(s\)")
        with open(self.get_log_path(), "r") as f:
            line = ""
            for line in f:
                if "%Warning-" in line:
                    warnings_count += 1
                if "Error-NEEDTIMINGOPT" in line:
                    timing_constructs = 1

            if not clean_exit:
                matched_errors = error_pattern.match(line)
                if matched_errors:
                    errors_count = int(matched_errors.group(1))
                else:
                    raise StepError("Linter exited non-cleanly")

        metrics_updates.update({"design__lint_errors__count": errors_count})
        metrics_updates.update(
            {"design__lint_timing_constructs__count": timing_constructs}
        )
        metrics_updates.update({"design__lint_warnings__count": warnings_count})
        return views_updates, metrics_updates

    def layout_preview(self) -> Optional[str]:
        return None
