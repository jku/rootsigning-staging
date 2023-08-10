# rootsigning staging Import process

This documents the import process for this repository.

The starting point is the "static" repository in https://github.com/sigstore/root-signing.git staging/ subdirectory:
All keys are file-based keys committed in the repository, there are no automated maintenance processes.

The goal is:
* A separate tuf-on-ci managed repository that can be used to test out new ideas in the sigstore rootsigning
  trust root delivery system 
* Processes that are closer to the production rootsigning processes
* An example to later move the production rootsigning repository to tuf-on-ci as well


### Import process steps (This is currently being tested)

#### Preparation

* Commit 1: Initialize repository by forking template tuf-on-ci-template
* Commit 2: Copy metadata from https://github.com/sigstore/root-signing.git: contents match staging/repository/ but filenames have been changed:
  * metadata files do not have versions (except in root_history/)
  * target files do not have hash prefixes
  * root versions stored in root_history/
* Commit 3: Rewrite all files with python-tuf (This is just whitespace changes and not strictly necessary
  but makes signing event review easier). See prep.py.
* Make old root private key available locally as import/import_root_priv.pem (this is from staging/keys/76651934/ in root-signing repository)
* Push changes to remote main: From now on we will use tuf-on-ci so remote branches matter
* Created local .tuf-on-ci-sign.ini config file where the only non-standard thing is signing-keys config: 
  The original root key is a private-key-in-file so needs config to be found:
  ```
  [signing-keys]
  c8e09a68b5821b75462ae0df52151c81deb7f1838246dc1da8c34cc91ec12bda = file:import/import_root_priv.pem?encrypted=false
  ```

#### Import

Now we create the first signing event where the goal is to
1. Add all of the custom metadata that tuf-on-ci needs to operate
2. Change all keys to ones managed by tuf-on-ci tooling

Steps
* Run `tuf-on-ci-import-repo sign/import` to get the required configuration 
* Create a file with import configuration, see import/import-config.json
* run `tuf-on-ci-import-repo sign/import import/import-config.json` to apply the config

