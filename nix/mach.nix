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
{
  pkgs,
  python-pname
}:

import (pkgs.fetchgit {
  url = "https://github.com/DavHau/mach-nix";
  rev = "70daee1b200c9a24a0f742f605edadacdcb5c998";
  sha256 = "sha256-mia90VYv/YTdWNhKpvwvFW9RfbXZJSWhJ+yva6EnLE8=";
}) {
  python = python-pname;
  pypiDataRev = "b6825a54053b58bf92f7d301a2891729c66c04f4";
  pypiDataSha256 = "sha256:0amjl58ykqrkxdf1yynclm70zlr60j53wg2byvjzll75kvxvkx9p";
}