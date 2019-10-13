try:
    from .real import ExtraChallenge
except ImportError:
    from .stubbed import ExtraChallenge

challenge = ExtraChallenge()