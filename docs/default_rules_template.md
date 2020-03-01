# Default Game Parameters

{% for item in parameters %}
## `{{ item.rule }}`

{{ item.description }}

Default Values: {{ item.value }}

Possible Values: {{ item.possible_vals }}

Notes: {{ item.notes }}
{% endfor %}