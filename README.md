# Devpi Resource

A [Concourse CI](http://concourse.ci) resource to track packages from the [devpi](http://doc.devpi.net/latest/) server.

## Source Configuration

* `uri`: *Required*. The base URI of the devpi server.
* `index`: *Required*. The package index in the form `user/name`.
* `package`: *Required*. The pacakge to track.
* `username`: *Optional*. The username for logging in (Required for `out`)
* `password`: *Optional*. The password for logging in (Required for `out`)
* `versioning`: *Optional*. The versioning scheme. Can be one of 'loose' (the default) or 'semantic'.

### Example

Resource configuration:

``` yaml
resources:
- name: my-package
  type: devpi
  source:
    uri: http://pypi.host.tld:9090
    index: foo/dev
    package: my-package-name
    username: user
    password: passwd
    versioning: semantic
```

Fetching a package:

``` yaml
- get: my-package
```

Pushing a local pacakge to the server:

``` yaml
- put: my-package
  params: {fileglob: "*.whl"}
```

The package to upload would usually be produced in a previous task of the job, e.g. by
running `python setup.py bdis_wheel`. So a minimal job for uploading a package to your
devpi-server would look like

```yaml
- name: package
  plan:
  - get: repo
    trigger: true
  - get: builder-image
  - task: build-package
    file: repo/ci/tasks/build-package.yml
    image: builder-image
```

whereas the `build-package.yml` could look like

```yaml
platform: linux
inputs:
- {name: repo}
outputs:
- {name: wheel}
run:
  path: ci/scripts/build-package.sh
  dir: repo
  args: [../wheel]
```

and your `build-package.sh` like this

```sh
#!/bin/sh

python setup.py bdist_wheel -d ${1}
```

## Behavior

### `check`: Check for new versions

The devpi server will be queried for new versions of the specified package.


### `in`: Pull a package from the devpi server

Downloads the package to the destination

#### Paramters

* `version`: *Optional*. Pull this specific version of the package instead of the newest.


### `out`: Push a package to the devpi server

#### Parameters

* `file`: Specifiy a concrete package filename to push to the server.
* `fileglob`: Specifiy a glob-pattern for matching files in the destination directory to
  be pushed to the server. The matched files are sorted alphanumerically and the "newest" is
  selected.
