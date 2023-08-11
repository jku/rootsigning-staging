# root-signing staging import process

This documents the import process for this repository.

The starting point is the "static" repository in https://github.com/sigstore/root-signing.git staging/ subdirectory:
All keys are file-based keys committed in the repository, there are no automated maintenance processes.

The goal is:
* A separate tuf-on-ci managed repository that can be used to test out new ideas in the sigstore rootsigning
  trust root delivery system 
* Processes that are closer to the production rootsigning processes
* An example to later move the production rootsigning repository to tuf-on-ci as well
* uninterrupted service for staging using sigstore clients

:warning: This import process is still under development

### Import process steps

#### Preparation

* Initialize repository by forking template tuf-on-ci-template
  * Modify the default publishing directories to match the ones sigstore uses (metadata: "", targets: "targets")
* Copy metadata from https://github.com/sigstore/root-signing.git: contents match staging/repository/ but filenames have been changed:
  * metadata files do not have versions (except in root_history/)
  * target files do not have hash prefixes
  * root versions stored in root_history/
* Rewrite all files with python-tuf (This is just whitespace changes and not strictly necessary
  but makes signing event review easier). See prep.py.
* Make old root private key available locally as import/import_root_priv.pem (this is from staging/keys/76651934/ in root-signing repository)
* Push changes to remote main: From now on we will use tuf-on-ci so remote branches matter
* Created local .tuf-on-ci-sign.ini config file where the non-standard things relate to signing-keys config: 
   The original root key is a private-key-in-file so needs config to be found:
  ```
  [signing-keys]
  c8e09a68b5821b75462ae0df52151c81deb7f1838246dc1da8c34cc91ec12bda = file:import/import_root_priv.pem?encrypted=false
  ```
  I also want to add my own hardware key as root signer and unfortunately tuf-on-ci currently only handles one key per role per user...
  So I use a temporary username to match the old signing key to: `user-name = @-repo-import`

#### Initial import

As user @-repo-import, add all of the custom metadata that tuf-on-ci needs to operate:
* Run `tuf-on-ci-import-repo sign/import` to get the required configuration 
* Create a file with import configuration, see import/import-config.json
* run `tuf-on-ci-import-repo sign/import import/import-config.json` to apply the config


#### Key changes

As myself (@jku), I add myself as signer. In practice this is easiest in a new git clone with a new .tuf-on-ci.ini file -- this way I have separate directories for the two users. In this .tuf-on-ci.ini I use my own github username and no configured signing-keys.

```
# Add myself as 2nd root signer
tuf-on-ci-delegate sign/initial-import root
# Make myself to sole signer for targets and npmjs
tuf-on-ci-delegate sign/initial-import targets
tuf-on-ci-delegate sign/initial-import registry.npmjs.org
# Setup proper online signing (using sigstore in this example even if it's not a good idea for a sigstore trust root :) )
tuf-on-ci-delegate sign/initial-import timestamp
```

Note that I do not remove the @-repo-import user as root signer: Normally tuf-on-ci would manage this just fine but in the import case
the removal needs to happen in another signing event

#### Final signature from original root key

As the import user:

```
tuf-on-ci-sign sign/initial-import
```

At this point signing event is finished and is ready to merge

