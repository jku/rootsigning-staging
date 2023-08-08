# rootsigning staging

This is an experiment to run the sigstore staging TUF repository with [repository-playground](https://github.com/jku/repository-playground/blob/main/playground/).


### Import process

(This is currently being tested)

* Commit 1: Initialize repository by using template tuf-on-ci-template
* Commit 2: Copy metadata from https://github.com/sigstore/root-signing.git: contents match staging/repository/ but filenames have been changed.
  * metadata files do not have versions (except in root_history/)
  * target files do not have hash prefixes
* Commit 3: Rewrite all files with python-tuf (This is just whitespace changes and not strictly necessary
  but makes signing event review easier). See prep.py. import could handle this?
* Push changes to remote main: From now on we will use tuf-on-ci so remote branches matter
* Create .tuf-on-ci-sign.ini config file. The original root key is a private-key-in-file so
  needs config to be found:
  ```
  [signing-keys]
  c8e09a68b5821b75462ae0df52151c81deb7f1838246dc1da8c34cc91ec12bda = file:importkey.pem?encrypted=false
  ```
* Make old root private key available locally as importkey.pem. See staging/keys/76651934/ in root-signing repository)
* Import signing event
  * Run tuf-on-ci-import to see required import configuration 
  * Create a file with import configuration, see import-config.json
    * the original root signing key must be available during the signing event.
    * the other key config is just there to make the import succeed: the keys will get changed during the signing event
  * run tuf-on-ci-import-repo with the file
  * change the keys to new keys using tuf-on-ci-delegate
    * root & targets key
    * online keys
    * registry.npmjs.org key
  * 
