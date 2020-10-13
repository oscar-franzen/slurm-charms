# charm-slurmctld
  
![alt text](.github/slurm.png)

<p align="center"><b>This is The Slurmctld charm for The Slurm Workload Manager</b>, <i>"The Slurm Workload Manager (formerly known as Simple Linux Utility for Resource Management or SLURM), or Slurm, is a free and open-source job scheduler for Linux and Unix-like kernels, used by many of the world's supercomputers and computer clusters."</i></p>

## Quickstart
```bash
juju deploy slurmctld
```

## Log level
The level of detail to provide slurmd daemon''s logs. The default value is `info`. Valid choices are: `quiet` (log nothing), `fatal` (log only fatal errors), `info` (log errors and general information messages), `verbose` (log errors and verbose informational messages). Then there are five debug levels which will be increasingly noisy (errors + noise): `debug`, `debug1`, `debug2`, `debug3`, `debug4`, `debug5`.

```bash
juju config slurmctld log_level=debug
```

## Process tracker
The default process tracker is now using cgroup (seems to better prevent orphan processes).

Change using:

```bash
# default
juju config slurmctld proctrack_type='proctrack/cgroup'

# not rcommended
juju config slurmctld proctrack_type='proctrack/linuxproc'
```

## Development
```bash
git clone git@github.com:omnivector-solutions/charm-slurmctld && cd charm-slurmctld
charmcraft build
juju deploy ./slurmctld.charm --resource slurm=/path/to/slurm.tar.gz
```
## Interfaces
- https://github.com/omnivector-solutions/interface-slurmd
- https://github.com/omnivector-solutions/ops-interface-slurmdbd

## Components
- https://github.com/omnivector-solutions/slurm-ops-manager
