from tuf.api.metadata import Metadata
from tuf.api.serialization.json import JSONSerializer


for rolename in ["root", "timestamp", "snapshot", "targets", "registry.npmjs.org"]:
    md: Metadata = Metadata.from_file(f"metadata/{rolename}.json")
    md.to_file(f"metadata/{rolename}.json", JSONSerializer())
