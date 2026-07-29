import models

string_fields = models.Headers.target_names_from_dtype('string')
original_headers = models.Headers.original_headers()
rename_map = models.Headers.rename_map()

print(string_fields)
print(original_headers)
print(rename_map)