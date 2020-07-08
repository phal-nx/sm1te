# Database Constants
HOST_IDENTIFIER = 'HostIdentifier'
HOST_DETAILS = 'HostDetails'
NODE_KEY = 'NodeKey'
QUERIES = 'Queries'
STATUSES = 'Statuses'


# Every 1 minutes give the diff
# Every day give the full list of installed packages
OSQUERY_CONFIGURATION = {
    "apt_packages_incremental": {
        "query": "SELECT name, version FROM deb_packages;",
        "interval": 60,
        "description": "Display diff of apt package manager sources.",
        "snapshot": False,
        "platform": "ubuntu"
    },
    "apt_packages": {
        "query": "SELECT name, version FROM deb_packages;",
        "interval": 864200,
        "description": "Display full apt package manager sources.",
        "snapshot": True,
        "platform": "ubuntu"
    },
    "rpm_packages_incremental": {
        "query": "SELECT name, version FROM rpm_packages;",
        "interval": 60,
        "description": "Display diff of apt package manager sources.",
        "snapshot": False,
        "platform": "redhat"
    },
    "rpm_packages": {
        "query": "SELECT name, version FROM rpm_packages;",
        "interval": 864200,
        "description": "Display full apt package manager sources.",
        "snapshot": True,
        "platform": "redhat"
    }
}
