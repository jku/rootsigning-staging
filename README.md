# rootsigning staging

This is an experiment to run the sigstore staging TUF repository with [TUF-on-CI](https://github.com/theupdateframework/tuf-on-ci/).

Note that _staging_ refers to a TUF repository that is completely separate from the production TUF repository (in other words it is not a staging phase of the production repository release process) -- the name might get changed to be less misleading but it comes from the directory name used in the sigstore rootsigning git tree: https://github.com/sigstore/root-signing/tree/main/staging
