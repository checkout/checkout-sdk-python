---
id: logging
title: Logging
---

### Logging

```python
os.environ['CKO_LOGGING'] = 'debug|DEBUG|info|INFO'
```

or ...

```python
import logging
logging.getLogger('cko').setLevel(logging.DEBUG)
```