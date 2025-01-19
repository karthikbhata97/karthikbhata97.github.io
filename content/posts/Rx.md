+++
date = 2024-01-19
draft = false
title = 'Rx: Treating Bugs As Allergies— A Safe Method to Survive Software Failures'
weight = 10
tags = ["paper-summary"]
+++

> Paper: [Rx: Treating Bugs As Allergies— A Safe Method to Survive Software Failures](https://dl.acm.org/doi/pdf/10.1145/1095810.1095833)

- Software failure recovery to make the softwares more available
- Makes use of Checkpointing and Rollback to revert to an older state
- Then makes some *environmental changes* and continues the execution of the application.
	- If none of the changes work, it goes back one more checkpoint and retries
- Components
	- Proxy: Separates client and server interactions and helps in the saving and replay of requests upon re-execution.
	- Sensors: Identifies when there is an error in the application using exceptions, interrupts etc.
	- Checkpointing and Rollback
		- Based on: [Flashback](https://www.usenix.org/legacy/event/usenix04/tech/general/full_papers/srinivasan/srinivasan.pdf)
		- Deletes oldest checkpoint based on stratergies.
	- Environmental wrappers: For modifying environment during re-execution
		- Memory allocation wrappers: eg: zero fill, add padding
		- Scheduling wrapper to change the unit of time for scheduling
		- User request dropping
	- Control unit: Coordinates with all the components
		- Also provides useful information for the programmer to diagnose and fix errors.
- Tested on Squid, Apache, CVS, MySQL
