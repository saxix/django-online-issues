#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    here = Path(__file__).parent
    sys.path.insert(0, str(here.parent.parent / "src"))
    sys.path.insert(0, str(here))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
