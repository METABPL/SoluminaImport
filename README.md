# Solumina Import

This repository contains a class model of how we currently map
a Solumina export into Python. The `load_solumina` module contains
a `load_process` function that takes the name of an XML export
file and returns a Process object representing that export
as a Process.

For example:
```Python
load_solumina.load_process("some_export.xml")
```

