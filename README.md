# SCASS

This is a README file for SCASS (SCAda Systems Security), developed by G. Capodagli with DIETI, University of Naples Federico II. SCASS is a hybrid testbed for ICSs (Industrial Control Systems).

## Getting Started

Clone the repository.

Software required:
* Python 3.6 or higher
* Docker

### Installing Python dependencies
With Python installed, run:
```
$ pip install -r requirements.txt
```

### Running virtual components

In _scass_ directory, run:
```
$ docker compose up
```

#### False Data Injection

In _scapy/fdi_ directory, files to execute a FDI attack towards the target architecture are located.


#### Denial of Service

In _scapy/dos_ directory, files to execute a DoS attack towards the target architecture are located.

## Threat Analysis

Threat analysis operations have been performed using STAMP/STPA and _MulVal_.

### Running MulVal for attack graph generation

in _ag_ directory, run:
```
$ ./genScript.sh
```

_genScript.sh_ deploys a Docker container in which _MulVal_ is installed and performs the generation of an attack graph on _interaction_rules_def.P_ and _scass.pl_ files.
