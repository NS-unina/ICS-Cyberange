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

### ACCIDENTS 

A<sub>1</sub>: uncontrolled generator overload (with damage)

A<sub>2</sub>: unwanted generator shutdown 

A<sub>3</sub>: physical damage to terminal operator 

A<sub>4</sub>: physical damage to gPLC 

A<sub>5</sub>: physical damage to G-IED1 

A<sub>6</sub>: physical damage to G-IED2


### HAZARDOUS CONTROL ACTIONS LEADING TO A<sub>1</sub>, A<sub>2</sub> 

HCA<sub>1</sub>: CA<sub>1</sub> is applied with incorrect parameters, shutting down the generator controlled by G-IED1 -> H<sub>3</sub>, H<sub>4</sub>

HCA<sub>2</sub>: CA<sub>1</sub> is applied with incorrect parameters, shutting down the generator controlled by G-IED2 -> H<sub>3</sub>, H<sub>5</sub> 

HCA<sub>3</sub>: CA<sub>2</sub> is applied with incorrect parameters, shutting down the generator -> H<sub>3</sub>, H<sub>4</sub>, H<sub>5</sub> 

HCA<sub>4</sub>: F<sub>2</sub> is applied with incorrect parameters, giving incorrect feedback to the operator -> H<sub>1</sub>

HCA<sub>5</sub>: F<sub>3</sub> is applied with incorrect parameters, giving incorrect feedback to gPLC -> H<sub>1</sub>, H<sub>2</sub> 

HCA<sub>6</sub>: F<sub>4</sub> is applied with incorrect parameters, giving incorrect feedback to gPLC -> H<sub>1</sub>, H<sub>2</sub> 

HCA<sub>7</sub>: CA<sub>3</sub> is applied with incorrect parameters, causing generator to deviate from steady state -> H<sub>4</sub>

HCA<sub>8</sub>: CA<sub>4</sub> is applied with incorrect parameters, causing generator to deviate from steady state -> H<sub>5</sub>


### HAZARDS 

H<sub>1</sub>: MASTER not synchronized with physical process

H<sub>2</sub>: gPLC not synchronized with physical process 

H<sub>3</sub>: unsafe configuration of gPLC 

H<sub>4</sub>: unsafe configuration of G-IED1 

H<sub>5</sub>: unsafe configuration of G-IED2 

| boh |   |   |   |   |
|-----|---|---|---|---|
|     |   |   |   |   |
|     |   |   |   |   |
|     |   |   |   |   |
