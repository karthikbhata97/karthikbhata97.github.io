+++
date = 2024-01-19
draft = false
title = 'Early Detection of Configuration Errors to Reduce Failure Damage'
weight = 10
tags = ["paper-summary"]
+++

> Paper: [Early Detection of Configuration Errors to Reduce Failure Damage](https://www.usenix.org/system/files/conference/osdi16/osdi16-xu.pdf)

- Defines `Latent Configuration (LC) Errors` which are caused due to insufficient validations on the configuration, later until the configuration is actually used
	- There might be a large time between loading this configuration, generally in the initialization phase, to actually using it (thus latent).
- When such configurations are related to reachability, availability or serviceability, LC errors can lead to downtime.
- Two main issues with such configs
	- The values are not checked at all. eg: check if file exists 
	- The values are not checked according to the usage. eg: value is used in open(config_value, WRITE)
- Paper implements a checker based on the static analysis and instrumentation
- Static analysis:
	- Taint analysis to go from the configuration to the actual usage along the data flow path. Control flow is ignored in most cases to avoid over tainting
	- Along with these instruction, the dependent values are also extracted. Eg: open(config_value, permission) <- here permission is dependent value
	- Any value that cannot be determined are skipped. Eg: a dependent value read from network
- Instrumentation:
	- Code is generated to perform same check as that in the actual usage, but in a "sandboxed" manner
	- Here any side effect on the program is avoided. Eg: a local copy of global value is used instead of the actual global value.
	- Utilities are written to check the actions performed by some library and system calls.
- This generated code is run right after the initialization phase of the program
	- Developer need to annotate two things
		- The interface of how configuration values are fetched
		- The place where program moves from initialization state to execution
- TOCTOU issues are avoided by adding support to run these checkers regularly in a thread
