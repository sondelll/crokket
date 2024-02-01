VERSION = {
    "major":0,
    "minor":7,
    "patch":0
}


class Version:
    def __init__(self, major:int, minor:int, patch:int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch
    def __str__(self):
        return f"Version {self.major}.{self.minor}.{self.patch}"

    
def get_version_str() -> str:
    v = Version(VERSION['major'], VERSION['minor'], VERSION['patch'])
    return str(v)
