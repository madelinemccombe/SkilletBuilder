# 12-12-19 nembery@paloaltonetworks.com
from skilletlib import Panoply
import os
import sys
import re

# grab our two configs from the environment
base_config_path = os.environ.get('BASE_CONFIG', '/Users/nembery/PycharmProjects/skilletlib/local_t/generate_skillet/config-01.xml')
latest_config_path = os.environ.get('LATEST_CONFIG', '/Users/nembery/PycharmProjects/skilletlib/local_t/generate_skillet/config-02.xml')

with open(base_config_path, 'r') as bcf:
    base_config = bcf.read()

with open(latest_config_path, 'r') as lcf:
    latest_config = lcf.read()

# init the Panoply helper class, note we do not need connection information, as we only need offline mode
# to compare two configurations
p = Panoply()

# insert magic here
snippets = p.generate_skillet_from_configs(base_config, latest_config)

# check we actually have some diffs
if len(snippets) == 0:
    print('No Candidate Configuration can be found to use to build a skillet!')
    sys.exit(2)


latest_config_html = latest_config.replace('<', '&lt;').replace('>', '&gt;')
for s in snippets:
    element_html = s.get('element', '').replace('<', '&lt;').replace('>', '&gt;')
    element_wrapped = f"<span class='text-danger'>{element_html}</span>"
    latest_config_html = latest_config_html.replace(element_html, element_wrapped)

print('<code type="xml">')
print(latest_config_html)
print('</code>')
# later gator
sys.exit(0)
