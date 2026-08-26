# Queue root placeholder

This tracked directory contains documentation only. Runtime queue roots are
created outside tracked fixtures and contain `work-orders/` plus `events/`.

Do not commit live work orders, credentials, provider data, or generated queue
state. Tests must use temporary directories.
