#!/usr/bin/env python

import os

from openapi_parser import parse

from ansible.module_utils.basic import AnsibleModule

def main():
  args = dict(
    spec=dict(type='path', required=True)
  )

  result = dict(endpoints=[])

  module = AnsibleModule(
    argument_spec=args,
    supports_check_mode=True
  )

  if not os.path.isfile(module.params['spec']):
    module.fail_json(msg="file %s not found" % (module.params['spec']), **result)

  spec = parse(module.params['spec'])

  for path in spec.paths:
    for operation in path.operations:
      endpoint = dict(method=operation.method.name, url=path.url)

      endpoint['query_params'] = get_query_params(operation.parameters)

      result['endpoints'].append(endpoint)

  module.exit_json(**result)

def get_query_params(parameters):
  params = []

  for param in parameters:
    if param.location.name == "QUERY":
      params.append(param.name)

  return params

if __name__ == '__main__':
  main()
