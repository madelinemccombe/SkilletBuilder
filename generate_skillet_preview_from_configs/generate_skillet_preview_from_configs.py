# 12-12-19 nembery@paloaltonetworks.com
from skilletlib import Panoply
import os
import sys
import re
from xml.etree import ElementTree

# grab our two configs from the environment
base_config_path = os.environ.get('BASE_CONFIG', '/Users/nembery/Downloads/sdwan_stage1.xml')
latest_config_path = os.environ.get('LATEST_CONFIG', '/Users/nembery/Downloads/sdwan_final_test.xml')

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

latest_doc = ElementTree.fromstring(latest_config)
latest_config_html = latest_config.replace('<', '&lt;').replace('>', '&gt;')
print('#'*80)
print('The following xpaths were found to be modified')

for s in snippets:
    name = s.get('name', '')
    full_xpath = s.get('xpath')
    print(f'<a href="#{name}">{full_xpath}</a>')
    xpath = re.sub('^/config', '', full_xpath)
    parent_element_xpath = '.' + "/".join(xpath.split('/')[:-1])
    parent_element = latest_doc.find(parent_element_xpath)
    parent_element_string = ElementTree.tostring(parent_element).decode('UTF-8')\
        .replace('<', '&lt;').replace('>', '&gt;')

    element_html = s.get('element', '').replace('<', '&lt;').replace('>', '&gt;')
    element_wrapped = f"<span id='{name}'class='text-danger' title='{full_xpath}'>{element_html}</span>"
    if element_html not in parent_element_string:
        print(f'{name} was not found in parent')
    parent_element_html = parent_element_string.replace(element_html, element_wrapped)

    latest_config_html = latest_config_html.replace(parent_element_string, parent_element_html)

print('-'*80)
print(latest_config_html)
print('-'*80)
print('#'*80)

# later gator
sys.exit(0)
