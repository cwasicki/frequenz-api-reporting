# Frequenz Reporting API Release Notes

## Summary

- `List*` endpoints have been removed.
- `MetricSourceOptions` have been renamed to `MetricConnections`, and moved out of the filter message.

## Upgrading

- Servers should remove the list endpoint implementations, clients should use the streaming endpoints.
- Metric source info can be found directly on the request, instead of in the filter object.

## New Features

<!-- Here goes the main new features and examples or instructions on how to use them -->

## Bug Fixes

<!-- Here goes notable bug fixes that are worth a special mention or explanation -->
