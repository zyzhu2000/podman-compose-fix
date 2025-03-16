# Introduction

In a YAML "compose" file, the path of the Dockerfile is often specified as a relative path to the location of the YAML "compose" file itself using the `context` keyword. When using `docker-compose` with the VSCode dev container, VSCode will first call `docker-compose config` to expand the relative paths to absolute paths and then use the resulting absolute paths to locate the Dockerfiles to build.

However, `podman-compose config` is not fully implemented. It simply prints out the YAML file verbatim without any normalization. If we use `podman-compose` as a replacement for `docker-compose`, since VSCode does not set the current directory to that of the YAML "compose" file when it tries to find the Dockerfiles, the lack of normalization causes it to fail to find them using the relative paths.

This script is a wrapper around `podman-compose`. It intercepts the `podman-compose config` command and will normalize any relative path specified with the `context` keyword in the YAML "compose" file. For any other commands, it simply calls the original `podman-comose`. It is a stopgap until `pdoman-compose` fully implements the `config` command.

# How to use

To use it, we need to set it up such that both VSCode and `podman compose` will call this script instead of the original `podman-compose`.

## VSCode

In the Dev Container extension setting, set Dev > Containers > Docker Compose Path, set it to this script.

## podman compose

For rootless containers, in `~/.config/containers/containers.conf`, add the following:
```
[engine]
compose_providers=['/path/to/this/script']
```
For details, see `man containers.conf(5)`.
