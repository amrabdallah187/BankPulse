# scripts/setup_ge_context.py
from great_expectations.data_context import get_context

# This will auto-generate great_expectations.yml if it doesn’t exist
context = get_context(mode="file")

print("✅ Great Expectations context initialized at ./great_expectations")
print("Config file:", context.root_directory + "/great_expectations.yml")
