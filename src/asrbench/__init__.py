"""asrbench: reproducible multilingual ASR evaluation for the course project.

Pipeline: dataset manifest -> `asrbench run` (raw predictions + run manifest)
-> `asrbench score` (per-language metrics, uncertainty, silence report) -> `asrbench compare`.
"""

__version__ = "0.1.0"
